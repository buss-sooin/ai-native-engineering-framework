import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import directive
from directive_conformance import validate_directive_conformance
import engine
import integration
from schema_validation import load_json


def known(value):
    return {'state': 'KNOWN', 'value': value}


def nr():
    return {'state': 'NOT_REQUIRED'}


def human_semantics(kind):
    return known({
        'goal': 'Perform ' + kind + ' with direct human responsibility.',
        'primary_operational_interface': 'Human IDE / Terminal',
        'what_to_observe': ['Observe the requested action and its verification evidence.'],
        'human_decision_required': 'Decide whether the observed result satisfies the approved boundary.',
        'expected_interpretation': 'A conforming result permits return to the named verification owner.',
        'cli_fallback': known('Use the approved low-level command only when the primary interface is insufficient.'),
    })


class IntegrationTests(unittest.TestCase):
    def setUp(self):
        self.profile = load_json(ROOT / 'profiles/framework-lab.v0.2.0.json')
        self.request = load_json(ROOT / 'tests/fixtures/inspection.request.json')

    def assert_no_directive(self, envelope):
        self.assertIsNone(envelope['directive'])
        self.assertEqual(envelope['emission_outcome'], 'BLOCKED')

    def humanize(self, request, basis, reevaluated=nr(), semantics=None):
        action = request['required_actions'][0]
        action.update(actor=known('HUMAN'), human_direct=known(True),
                      human_necessity_basis=known(basis) if basis else {'state': 'UNKNOWN'},
                      targeted_re_evaluation_established=copy.deepcopy(reevaluated),
                      human_facing_semantics=human_semantics(action['kind']['value']) if semantics is None else semantics,
                      session_role=known('Human Execution Operator'))
        request['surface_selection'] = known([{'action_id': action['id'], 'surface_id': 'human-terminal'}])
        return request

    def make(self, *kinds):
        request = copy.deepcopy(self.request)
        request['required_actions'] = []
        effects = set()
        for index, kind in enumerate(kinds):
            definition = next(item for item in self.profile['actions'] if item['kind'] == kind)
            required = definition['authority_required']
            human = definition['actor'] == 'HUMAN'
            effects.update(definition['effects'])
            request['required_actions'].append({
                'id': 'a' + str(index), 'kind': known(kind), 'actor': known(definition['actor']),
                'authority': 'AUTHORIZED' if required else 'NOT_REQUIRED',
                'approval_reference': known('fixture approval') if required else {'state': 'NOT_REQUIRED'},
                'target': copy.deepcopy(request['target']), 'effects': known(definition['effects']),
                'source_references': known(['fixture:' + kind]),
                'human_direct': known(human),
                'human_necessity_basis': known('DIRECT_HUMAN_OBSERVATION_OBJECTIVE' if kind == 'observe_runtime'
                                                else 'HUMAN_RISK_CONTROL_REQUIRED') if human else nr(),
                'targeted_re_evaluation_established': nr(),
                'human_facing_semantics': human_semantics(kind) if human else nr(),
                'verification_requirement': known(['Verify ' + kind]),
                'session_role': known('Human Operator' if human else 'AI Reviewer'),
            })
        request['approved_execution_boundary'] = known({
            'target': request['target']['value'],
            'allowed_action_ids': [item['id'] for item in request['required_actions']],
            'allowed_effects': sorted(effects)})
        request['prohibited_actions'] = known([])
        return request

    def test_contract_preservation_for_representative_routes(self):
        routes = (('reason_context',), ('inspect_repository',), ('mutate_repository',),
                  ('observe_runtime',), ('observe_runtime', 'inspect_repository'))
        for kinds in routes:
            with self.subTest(kinds=kinds):
                request = self.make(*kinds)
                standalone = engine.evaluate(request, self.profile)
                mediated = integration.integrate(request, self.profile)
                self.assertEqual(standalone['routing_status'], 'PASS')
                self.assertEqual(mediated['result'], standalone['result'])

        failed = copy.deepcopy(self.request)
        failed['surface_selection'] = known([{'action_id': 'inspect', 'surface_id': 'general-chat'}])
        unresolved = self.make('mutate_repository')
        unresolved['required_actions'][0].update(authority='UNKNOWN', approval_reference={'state': 'UNKNOWN'})
        for request in (failed, unresolved):
            with self.subTest(status=engine.evaluate(request, self.profile)['routing_status']):
                standalone = engine.evaluate(request, self.profile)
                mediated = integration.integrate(request, self.profile)
                self.assertEqual(mediated['result'], standalone['result'])

    def test_only_validated_pass_emits(self):
        envelope = integration.integrate(self.request, self.profile)
        self.assertEqual(envelope['integration_status'], 'PASS')
        self.assertEqual(envelope['routing_status'], 'PASS')
        self.assertEqual(envelope['directive_validation']['status'], 'PASS')
        self.assertEqual(envelope['emission_outcome'], 'EMITTED')
        self.assertTrue(envelope['directive'].startswith('## Routing Header\n'))

    def test_semantic_fail_and_unresolved_are_preserved(self):
        failed = copy.deepcopy(self.request)
        failed['surface_selection'] = known([{'action_id': 'inspect', 'surface_id': 'general-chat'}])
        fail_envelope = integration.integrate(failed, self.profile)
        self.assertEqual(fail_envelope['integration_status'], 'BLOCKED_BY_ROUTING')
        self.assertEqual(fail_envelope['routing_status'], 'FAIL')
        self.assertIn('SURFACE_CAPABILITY_MISMATCH', fail_envelope['failure_codes'])
        self.assert_no_directive(fail_envelope)

        unresolved = self.make('mutate_repository')
        unresolved['required_actions'][0]['authority'] = 'UNKNOWN'
        unresolved['required_actions'][0]['approval_reference'] = {'state': 'UNKNOWN'}
        unresolved_envelope = integration.integrate(unresolved, self.profile)
        self.assertEqual(unresolved_envelope['integration_status'], 'BLOCKED_BY_ROUTING')
        self.assertEqual(unresolved_envelope['routing_status'], 'UNRESOLVED')
        self.assert_no_directive(unresolved_envelope)

    def test_pcbw_r07_fail_and_unresolved_never_emit(self):
        failed = self.humanize(self.make('run_command'),
                               'NO_SUITABLE_AUTHORIZED_AI_SURFACE', known(True))
        fail_envelope = integration.integrate(failed, self.profile)
        self.assertEqual(fail_envelope['routing_status'], 'FAIL')
        self.assertIn('INVALID_HUMAN_DELEGATION', fail_envelope['failure_codes'])
        self.assert_no_directive(fail_envelope)

        unresolved = self.humanize(self.make('run_command'), 'HUMAN_AUTHORITY_REQUIRED')
        del unresolved['required_actions'][0]['human_necessity_basis']
        unresolved_envelope = integration.integrate(unresolved, self.profile)
        self.assertEqual(unresolved_envelope['routing_status'], 'UNRESOLVED')
        self.assertIn('HUMAN_NECESSITY_BASIS_MISSING',
                      {item['code'] for item in unresolved_envelope['unresolved_issues']})
        self.assert_no_directive(unresolved_envelope)

        insufficient = self.humanize(self.make('run_command'), 'HUMAN_RISK_CONTROL_REQUIRED')
        del insufficient['required_actions'][0]['human_facing_semantics']
        insufficient_envelope = integration.integrate(insufficient, self.profile)
        self.assertEqual(insufficient_envelope['routing_status'], 'FAIL')
        self.assertIn('HUMAN_FACING_SEMANTICS_INSUFFICIENT', insufficient_envelope['failure_codes'])
        self.assert_no_directive(insufficient_envelope)

    def test_pcbw_r07_legitimate_human_execution_emits_complete_semantics(self):
        request = self.humanize(self.make('run_command'), 'HUMAN_EXECUTION_SIMPLER_OR_SAFER')
        envelope = integration.integrate(request, self.profile)
        self.assertEqual(envelope['integration_status'], 'PASS', envelope)
        self.assertEqual(envelope['emission_outcome'], 'EMITTED')
        self.assertIn('## Human Execution Responsibility', envelope['directive'])
        self.assertIn('Primary Operational Interface / Tool', envelope['directive'])

    def test_pcbw_r07_human_semantics_drift_is_rejected_by_independent_validator(self):
        request = self.humanize(self.make('run_command'), 'HUMAN_AUTHORITY_REQUIRED')
        result = engine.evaluate(request, self.profile)['result']
        valid = directive.render(result)['directive']
        marker = '## Human Execution Responsibility'
        prefix, human_section = valid.split(marker, 1)
        changed = prefix + marker + human_section.replace(
            'Perform run_command with direct human responsibility.', 'Relay an unexplained command.', 1)
        validation = validate_directive_conformance(result, changed)
        self.assertEqual(validation['status'], 'FAIL')
        self.assertIn('HUMAN_EXECUTION_SEMANTICS_MISMATCH', validation['failure_codes'])

    def test_invalid_request_and_profile_are_integration_blocked(self):
        invalid_request = copy.deepcopy(self.request)
        del invalid_request['project']
        envelope = integration.integrate(invalid_request, self.profile)
        self.assertEqual(envelope['integration_status'], 'INTEGRATION_BLOCKED')
        self.assertEqual(envelope['integration_diagnostics'][0]['code'], 'ROUTING_REQUEST_INVALID')
        self.assert_no_directive(envelope)

        invalid_profile = copy.deepcopy(self.profile)
        invalid_profile['surfaces'].append(copy.deepcopy(invalid_profile['surfaces'][0]))
        envelope = integration.integrate(self.request, invalid_profile)
        self.assertEqual(envelope['integration_diagnostics'][0]['code'], 'ROUTING_PROFILE_INVALID')
        self.assert_no_directive(envelope)

    def test_engine_failures_are_integration_blocked(self):
        cases = (
            (None, 'ENGINE_UNAVAILABLE'),
            (lambda *_: (_ for _ in ()).throw(RuntimeError('fault')), 'ENGINE_INVOCATION_ERROR'),
            (lambda *_: {'routing_status': 'PASS'}, 'ENGINE_RESULT_INVALID'),
        )
        for callable_, code in cases:
            with self.subTest(code=code):
                envelope = integration.integrate(self.request, self.profile, engine_callable=callable_)
                self.assertEqual(envelope['integration_status'], 'INTEGRATION_BLOCKED')
                self.assertEqual(envelope['integration_diagnostics'][0]['code'], code)
                self.assert_no_directive(envelope)

    def test_renderer_and_validator_failures_are_integration_blocked(self):
        def raises(*_):
            raise RuntimeError('fault')

        cases = (
            ({'renderer_callable': None}, 'RENDERER_UNAVAILABLE'),
            ({'renderer_callable': raises}, 'RENDERER_ERROR'),
            ({'validator_callable': None}, 'DIRECTIVE_VALIDATOR_UNAVAILABLE'),
            ({'validator_callable': raises}, 'DIRECTIVE_VALIDATOR_ERROR'),
            ({'validator_callable': lambda *_: {'status': 'FAIL', 'failure_codes': ['fixture']}},
             'DIRECTIVE_CONFORMANCE_REJECTED'),
        )
        for kwargs, code in cases:
            with self.subTest(code=code):
                envelope = integration.integrate(self.request, self.profile, **kwargs)
                self.assertEqual(envelope['integration_status'], 'INTEGRATION_BLOCKED')
                self.assertEqual(envelope['integration_diagnostics'][0]['code'], code)
                self.assert_no_directive(envelope)

    def test_unknown_authority_and_unavailable_capability_never_emit(self):
        request = self.make('run_command')
        request['required_actions'][0].update(authority='UNKNOWN', approval_reference={'state': 'UNKNOWN'})
        self.assert_no_directive(integration.integrate(request, self.profile))

        profile = copy.deepcopy(self.profile)
        next(item for item in profile['surfaces'] if item['id'] == 'work-mode')['available'] = known(False)
        envelope = integration.integrate(self.request, profile)
        self.assertEqual(envelope['routing_status'], 'UNRESOLVED')
        self.assert_no_directive(envelope)

    def test_renderer_validator_independence_and_result_directive_mismatch(self):
        result = engine.evaluate(self.request, self.profile)['result']
        valid_text = directive.render(result)['directive']
        corrupt_text = valid_text.replace('ChatGPT Work mode', 'ChatGPT 일반 Chat')
        with patch('directive._render', return_value=corrupt_text):
            envelope = integration.integrate(self.request, self.profile)
        self.assertEqual(envelope['integration_status'], 'INTEGRATION_BLOCKED')
        self.assertIn('EXECUTION_SURFACE_MISMATCH', envelope['directive_validation']['failure_codes'])
        self.assert_no_directive(envelope)

    def test_historical_directive_failure_fixtures(self):
        result = engine.evaluate(self.request, self.profile)['result']
        valid = directive.render(result)['directive']
        fixtures = load_json(ROOT / 'tests/fixtures/historical-directive-failures.json')

        def mutate(kind):
            if kind == 'remove_header_marker':
                return valid.replace('## Routing Header\n', '', 1)
            if kind == 'move_header_after_body':
                marker = '\n# Repository inspection\n'
                header, body = valid.split(marker, 1)
                return '# Repository inspection\n' + body + '\n' + header + '\n'
            if kind == 'role_surface_conflation':
                return valid.replace('- Destination Session Role: "Repository Reviewer"',
                                     '- Destination Session Role: "ChatGPT Work mode"', 1)
            if kind in ('incorrect_execution_surface', 'surface_result_drift'):
                return valid.replace('"surface":"ChatGPT Work mode"',
                                     '"surface":"ChatGPT 일반 Chat"', 1)
            if kind == 'strengthen_authority':
                return valid.replace('"input_status":"NOT_REQUIRED"',
                                     '"input_status":"AUTHORIZED"', 1)
            if kind == 'omit_verification_section':
                start = valid.index('## Verification / Expected Result')
                end = valid.index('## Return / Closure Destination')
                return valid[:start] + valid[end:]
            raise AssertionError(kind)

        for fixture in fixtures:
            with self.subTest(fixture=fixture['id']):
                validation = validate_directive_conformance(result, mutate(fixture['mutation']))
                self.assertEqual(validation['status'], 'FAIL')
                self.assertIn(fixture['expected_code'], validation['failure_codes'])

    def test_title_responsibility_authority_and_extra_content_drift(self):
        result = engine.evaluate(self.request, self.profile)['result']
        text = directive.render(result)['directive']
        cases = (
            (text.replace('# Repository inspection', '# Changed title', 1), 'SESSION_TITLE_MISMATCH'),
            (text.replace('Project human owner', 'AI owner', 1), 'RESPONSIBILITY_MISMATCH'),
            (text.replace('"status":"NOT_REQUIRED"', '"status":"AUTHORIZED"', 1), 'AUTHORITY_MISMATCH'),
            (text + '\nExecute automatically.\n', 'UNEXPECTED_DIRECTIVE_CONTENT'),
        )
        for changed, code in cases:
            with self.subTest(code=code):
                validation = validate_directive_conformance(result, changed)
                self.assertEqual(validation['status'], 'FAIL')
                self.assertIn(code, validation['failure_codes'])

    def test_evidence_and_adapter_are_deterministic(self):
        first = integration.integrate(self.request, self.profile)
        second = integration.integrate(self.request, self.profile)
        self.assertEqual(first, second)
        evidence = first['evidence']
        self.assertEqual(evidence['emission_outcome'], 'EMITTED')
        for field in ('routing_request_fingerprint', 'routing_result_fingerprint',
                      'routing_semantic_fingerprint', 'rendered_directive_fingerprint',
                      'directive_validation_fingerprint'):
            self.assertRegex(evidence[field], r'^[0-9a-f]{64}$')

    def test_integration_cli_pass_and_invalid_serialization(self):
        command = [sys.executable, str(ROOT / 'src/integration_cli.py'),
                   '--request', str(ROOT / 'tests/fixtures/inspection.request.json'),
                   '--profile', str(ROOT / 'profiles/framework-lab.v0.2.0.json')]
        passed = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(passed.returncode, 0, passed.stdout)
        self.assertEqual(json.loads(passed.stdout)['integration_status'], 'PASS')
        with tempfile.TemporaryDirectory() as folder:
            invalid = Path(folder) / 'invalid.json'
            invalid.write_text('{"x":1,"x":2}', encoding='utf-8')
            failed = subprocess.run(command[:2] + ['--request', str(invalid)] + command[4:],
                                    capture_output=True, text=True)
            self.assertEqual(failed.returncode, 3, failed.stdout)
            envelope = json.loads(failed.stdout)
            self.assertEqual(envelope['integration_diagnostics'][0]['code'], 'REQUEST_SERIALIZATION_INVALID')
            self.assert_no_directive(envelope)


if __name__ == '__main__':
    unittest.main()
