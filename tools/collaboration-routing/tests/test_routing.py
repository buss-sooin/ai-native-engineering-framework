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
import engine
import directive
import directive_conformance
from schema_validation import InvalidDocument, SchemaError, check_schema, load_json, validate


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


class RoutingTests(unittest.TestCase):
    def setUp(self):
        self.profile = load_json(ROOT / 'profiles/framework-lab.v0.2.0.json')
        self.request = load_json(ROOT / 'tests/fixtures/inspection.request.json')

    def make(self, *kinds):
        request = copy.deepcopy(self.request)
        definitions = {a['kind']: a for a in self.profile['actions']}
        request['required_actions'] = []
        effects = set()
        for index, kind in enumerate(kinds):
            definition = definitions[kind]
            effects.update(definition['effects'])
            required = definition['authority_required']
            human = definition['actor'] == 'HUMAN'
            request['required_actions'].append({'id': 'a' + str(index), 'kind': known(kind),
                'actor': known(definition['actor']), 'authority': 'AUTHORIZED' if required else 'NOT_REQUIRED',
                'target': copy.deepcopy(request['target']), 'effects': known(definition['effects']),
                'source_references': known(['fixture:' + kind]), 'human_direct': known(human),
                'human_necessity_basis': known('DIRECT_HUMAN_OBSERVATION_OBJECTIVE' if kind == 'observe_runtime'
                                                else 'HUMAN_RISK_CONTROL_REQUIRED') if human else nr(),
                'targeted_re_evaluation_established': nr(),
                'human_facing_semantics': human_semantics(kind) if human else nr(),
                'verification_requirement': known(['Verify ' + kind + ' against the supplied target.']),
                'session_role': known('Human Runtime Operator' if human else 'AI Task Reviewer'),
                'approval_reference': known('fixture-only human approval; not live authorization') if required else nr()})
        request['approved_execution_boundary'] = known({'target': request['target']['value'],
            'allowed_action_ids': [a['id'] for a in request['required_actions']], 'allowed_effects': sorted(effects)})
        request['prohibited_actions'] = known([])
        return request

    def codes(self, envelope):
        return set(envelope['failure_codes']) | {i['code'] for i in envelope['unresolved_issues']}

    def humanize(self, request, basis, reevaluated=nr(), semantics=None):
        action = request['required_actions'][0]
        action.update(actor=known('HUMAN'), human_direct=known(True),
                      human_necessity_basis=known(basis) if basis else {'state': 'UNKNOWN'},
                      targeted_re_evaluation_established=copy.deepcopy(reevaluated),
                      human_facing_semantics=human_semantics(action['kind']['value']) if semantics is None else semantics,
                      session_role=known('Human Execution Operator'))
        request['surface_selection'] = known([{'action_id': action['id'], 'surface_id': 'human-terminal'}])
        return request

    def assertBlocked(self, envelope, status, code):
        self.assertEqual(envelope['routing_status'], status, envelope)
        self.assertIn(code, self.codes(envelope))
        self.assertIsNone(envelope['directive'])
        if envelope['result']:
            self.assertIsNone(directive.render(envelope['result'])['directive'])

    def test_mandatory_regressions(self):
        for fixture in load_json(ROOT / 'tests/fixtures/regressions.json'):
            with self.subTest(fixture=fixture['id']):
                request = self.make(fixture['kind'])
                if 'request_file' in fixture:
                    request = load_json(ROOT / 'tests/fixtures' / fixture['request_file'])
                profile = copy.deepcopy(self.profile)
                if 'selected' in fixture:
                    request['surface_selection'] = known([{'action_id': 'a0', 'surface_id': fixture['selected']}])
                if 'unavailable' in fixture:
                    next(s for s in profile['surfaces'] if s['id'] == fixture['unavailable'])['available'] = known(False)
                if 'authority' in fixture:
                    request['required_actions'][0]['authority'] = fixture['authority']
                if fixture.get('fault') == 'exception':
                    with patch('engine._evaluate', side_effect=RuntimeError('test fault')):
                        envelope = engine.evaluate(request, profile)
                else:
                    envelope = engine.evaluate(request, profile)
                if 'drift' in fixture:
                    self.assertEqual(envelope['routing_status'], 'PASS')
                    rendered = directive.render(envelope['result'])
                    before, after = fixture['drift']
                    self.assertIn(before, rendered['directive'])
                    envelope = directive.validate_directive(envelope['result'], rendered['directive'].replace(before, after))
                self.assertBlocked(envelope, fixture['expected'], fixture['code'])

    def test_all_normal_single_routes(self):
        expected = {'reason_context': 'general-chat', 'inspect_repository': 'work-mode', 'edit_document': 'work-mode',
                    'mutate_repository': 'codex', 'git_branch': 'codex', 'run_command': 'codex', 'run_tests': 'codex',
                    'observe_runtime': 'human-terminal', 'mutate_runtime': 'human-terminal'}
        for kind, surface in expected.items():
            with self.subTest(kind=kind):
                request = self.make(kind)
                validate(request, 'routing-request')
                engine.validate_profile(self.profile)
                first = engine.evaluate(request, self.profile)
                self.assertEqual(first['routing_status'], 'PASS', first)
                result = first['result']
                validate(result, 'routing-result')
                self.assertEqual(result['route_mode'], 'SINGLE')
                self.assertEqual(result['execution_plan'][0]['surface_id'], surface)
                self.assertEqual(first, engine.evaluate(request, self.profile))
                rendered = directive.render(result)
                self.assertEqual(rendered['routing_status'], 'PASS')
                self.assertEqual(rendered, directive.render(result))
                self.assertTrue(rendered['directive'].startswith('## Routing Header\n'))

    def test_composite_routes(self):
        for ai, expected in [('reason_context', 'general-chat'), ('inspect_repository', 'work-mode')]:
            for human in ('observe_runtime', 'mutate_runtime'):
                with self.subTest(ai=ai, human=human):
                    result = engine.evaluate(self.make(human, ai), self.profile)['result']
                    self.assertEqual(result['routing_status'], 'PASS')
                    self.assertEqual(result['route_mode'], 'COMPOSITE')
                    self.assertEqual({s['surface_id'] for s in result['execution_plan']}, {'human-terminal', expected})
                    text = directive.render(result)['directive']
                    self.assertIn('AI Session Surface', text)
                    self.assertIn('Human Execution Surface', text)

    def test_pcbw_r07_blocks_deterministic_human_command_relay(self):
        cases = (
            ('deterministic preflight', 'run_tests', 'Preflight Verification Runner',
             'Run the approved preflight verification before execution.'),
            ('repeated deterministic polling', 'run_command', 'Runtime State Poller',
             'Poll the bounded runtime predicate until it reaches a terminal state.'),
            ('deterministic reconciliation', 'run_command', 'Evidence Reconciliation Runner',
             'Reconcile the captured counts using the approved deterministic formula.'),
            ('bounded predicate-driven phase transition', 'run_command', 'Phase Transition Runner',
             'Apply the approved transition only when the explicit predicate is true.'),
            ('current Chat lacks shell while authorized Codex CLI is suitable', 'run_command',
             'Command Execution Runner', 'Execute the authorized command on Codex CLI.'),
        )
        for description, kind, role, verification in cases:
            with self.subTest(description=description):
                request = self.humanize(self.make(kind),
                                        'NO_SUITABLE_AUTHORIZED_AI_SURFACE', known(True))
                request['objective'] = known(description)
                request['required_actions'][0].update(
                    source_references=known(['PCBW-R07 regression: ' + description]),
                    session_role=known(role), verification_requirement=known([verification]))
                envelope = engine.evaluate(request, self.profile)
                self.assertBlocked(envelope, 'FAIL', 'INVALID_HUMAN_DELEGATION')

    def test_pcbw_r07_preserves_legitimate_human_direct_engineering(self):
        bases = (
            'HUMAN_AUTHORITY_REQUIRED',
            'DIRECT_HUMAN_OBSERVATION_OBJECTIVE',
            'HUMAN_RISK_CONTROL_REQUIRED',
            'HUMAN_LEARNING_OBJECTIVE',
            'HUMAN_EXECUTION_SIMPLER_OR_SAFER',
        )
        for basis in bases:
            with self.subTest(basis=basis):
                envelope = engine.evaluate(self.humanize(self.make('run_command'), basis), self.profile)
                self.assertEqual(envelope['routing_status'], 'PASS', envelope)
                self.assertEqual(envelope['result']['execution_plan'][0]['surface_id'], 'human-terminal')
                rendered = directive.render(envelope['result'])['directive']
                self.assertIn('## Human Execution Responsibility', rendered)
                self.assertIn('Human Goal', rendered)
                self.assertIn(basis, rendered)

    def test_pcbw_r07_no_suitable_ai_requires_targeted_re_evaluation(self):
        for reevaluated in ({'state': 'UNKNOWN'}, nr(), known(False)):
            with self.subTest(reevaluated=reevaluated):
                request = self.humanize(self.make('run_command'),
                                        'NO_SUITABLE_AUTHORIZED_AI_SURFACE', reevaluated)
                self.assertBlocked(engine.evaluate(request, self.profile), 'UNRESOLVED',
                                   'TARGETED_RE_EVALUATION_NOT_ESTABLISHED')

        profile = copy.deepcopy(self.profile)
        next(surface for surface in profile['surfaces'] if surface['id'] == 'codex')['available'] = known(False)
        request = self.humanize(self.make('run_command'),
                                'NO_SUITABLE_AUTHORIZED_AI_SURFACE', known(True))
        envelope = engine.evaluate(request, profile)
        self.assertEqual(envelope['routing_status'], 'PASS', envelope)
        self.assertEqual(envelope['result']['execution_plan'][0]['actor'], 'HUMAN')

        profile = copy.deepcopy(self.profile)
        next(surface for surface in profile['surfaces'] if surface['id'] == 'codex')['available'] = {'state': 'UNKNOWN'}
        request = self.humanize(self.make('run_command'),
                                'NO_SUITABLE_AUTHORIZED_AI_SURFACE', known(True))
        self.assertBlocked(engine.evaluate(request, profile), 'UNRESOLVED',
                           'TARGETED_RE_EVALUATION_NOT_ESTABLISHED')

        profile = copy.deepcopy(self.profile)
        profile['surfaces'].append({
            'id': 'ai-runtime-observer', 'label': 'AI Runtime Observer', 'actor': 'AI',
            'capabilities': ['runtime_observation'], 'available': known(True),
            'model_recommendation': 'Surface-managed / N/A',
            'reasoning_recommendation': 'Surface-managed / N/A',
            'supported_effects': ['RUNTIME_OBSERVATION'],
        })
        request = self.make('observe_runtime')
        request['required_actions'][0].update(
            human_necessity_basis=known('NO_SUITABLE_AUTHORIZED_AI_SURFACE'),
            targeted_re_evaluation_established=known(True))
        self.assertBlocked(engine.evaluate(request, profile), 'FAIL',
                           'NO_SUITABLE_AI_SURFACE_CONTRADICTION')

    def test_pcbw_r07_missing_basis_and_insufficient_semantics_block(self):
        request = self.humanize(self.make('run_command'), None)
        self.assertBlocked(engine.evaluate(request, self.profile), 'UNRESOLVED',
                           'HUMAN_NECESSITY_BASIS_MISSING')

        request = self.humanize(self.make('run_command'), 'HUMAN_AUTHORITY_REQUIRED')
        del request['required_actions'][0]['human_necessity_basis']
        self.assertBlocked(engine.evaluate(request, self.profile), 'UNRESOLVED',
                           'HUMAN_NECESSITY_BASIS_MISSING')

        request = self.humanize(self.make('run_command'), 'HUMAN_RISK_CONTROL_REQUIRED',
                                semantics={'state': 'UNKNOWN'})
        self.assertBlocked(engine.evaluate(request, self.profile), 'FAIL',
                           'HUMAN_FACING_SEMANTICS_INSUFFICIENT')

        request = self.humanize(self.make('run_command'), 'HUMAN_RISK_CONTROL_REQUIRED')
        del request['required_actions'][0]['human_facing_semantics']
        self.assertBlocked(engine.evaluate(request, self.profile), 'FAIL',
                           'HUMAN_FACING_SEMANTICS_INSUFFICIENT')

    def test_pcbw_r07_missing_targeted_re_evaluation_is_unresolved(self):
        request = self.humanize(self.make('run_command'),
                                'NO_SUITABLE_AUTHORIZED_AI_SURFACE', known(True))
        del request['required_actions'][0]['targeted_re_evaluation_established']
        self.assertBlocked(engine.evaluate(request, self.profile), 'UNRESOLVED',
                           'TARGETED_RE_EVALUATION_NOT_ESTABLISHED')

    def test_pcbw_r01_to_r06_legacy_action_shape_remains_accepted(self):
        for kind in ('reason_context', 'inspect_repository', 'run_command'):
            with self.subTest(kind=kind):
                request = self.make(kind)
                for field in ('human_necessity_basis', 'targeted_re_evaluation_established',
                              'human_facing_semantics'):
                    del request['required_actions'][0][field]
                self.assertEqual(engine.evaluate(request, self.profile)['routing_status'], 'PASS')

    def test_pcbw_r07_human_semantics_are_independently_protected(self):
        result = engine.evaluate(self.humanize(self.make('run_command'),
                                               'HUMAN_AUTHORITY_REQUIRED'), self.profile)['result']
        text = directive.render(result)['directive']
        changed = text.replace('Perform run_command with direct human responsibility.',
                               'Relay an unexplained command.', 1)
        self.assertBlocked(directive.validate_directive(result, changed), 'FAIL', 'MATERIAL_DIRECTIVE_DRIFT')

    def test_pcbw_r07_identifier_only_semantics_fail_closed(self):
        semantics = load_json(ROOT / 'tests/fixtures/identifier-only-human-semantics.json')
        request = self.humanize(self.make('run_command'), 'HUMAN_RISK_CONTROL_REQUIRED',
                                semantics=semantics)
        validate(request, 'routing-request')
        self.assertBlocked(engine.evaluate(request, self.profile), 'FAIL',
                           'HUMAN_FACING_SEMANTICS_INSUFFICIENT')

    def test_pcbw_r07_control_placeholder_and_mixed_semantics_fail(self):
        cases = (
            ('identifier-only', 'goal', 'FS-07'),
            ('status-only', 'human_decision_required', 'UNRESOLVED'),
            ('placeholder-only', 'expected_interpretation', 'TODO'),
            ('phase-gate-step-only', 'what_to_observe', ['Phase A Gate PASS STEP-3']),
            ('mixed-identifiers', 'goal', 'FS-07 C0 Gate PASS Phase A STEP-3'),
            ('identifier-interface', 'primary_operational_interface', 'C0'),
            ('placeholder-fallback', 'cli_fallback', known('TBD')),
        )
        for label, field, value in cases:
            with self.subTest(label=label):
                semantics = human_semantics('run_command')
                semantics['value'][field] = value
                request = self.humanize(self.make('run_command'), 'HUMAN_AUTHORITY_REQUIRED',
                                        semantics=semantics)
                self.assertBlocked(engine.evaluate(request, self.profile), 'FAIL',
                                   'HUMAN_FACING_SEMANTICS_INSUFFICIENT')

    def test_pcbw_r07_concise_operational_interfaces_remain_valid(self):
        for interface in ('MySQL Workbench', 'Grafana'):
            with self.subTest(interface=interface):
                semantics = known({
                    'goal': 'MySQL 복구 후 persistence가 정상 재개됐는지 판단한다.',
                    'primary_operational_interface': interface,
                    'what_to_observe': ['대상 barcode cohort가 실제 table에 저장되는지 확인한다.'],
                    'human_decision_required': '누락 없이 저장됐으면 persistence recovery complete로 판단한다.',
                    'expected_interpretation': 'DB health뿐 아니라 실제 persistence 결과까지 확인되어야 복구 완료다.',
                    'cli_fallback': nr(),
                })
                request = self.humanize(self.make('run_command'),
                                        'DIRECT_HUMAN_OBSERVATION_OBJECTIVE', semantics=semantics)
                envelope = engine.evaluate(request, self.profile)
                self.assertEqual(envelope['routing_status'], 'PASS', envelope)
                self.assertEqual(directive.render(envelope['result'])['routing_status'], 'PASS')

    def test_pcbw_r07_forged_pass_cannot_bypass_conformance_or_renderer(self):
        result = engine.evaluate(self.humanize(self.make('run_command'),
                                               'HUMAN_AUTHORITY_REQUIRED'), self.profile)['result']
        forged = copy.deepcopy(result)
        semantics = load_json(ROOT / 'tests/fixtures/identifier-only-human-semantics.json')
        forged['source_request']['required_actions'][0]['human_facing_semantics'] = copy.deepcopy(semantics)
        forged['execution_plan'][0]['assigned_actions'][0]['human_facing_semantics'] = copy.deepcopy(semantics)
        forged['semantic_fingerprint'] = engine.fingerprint(forged)
        forged['routing_result_id'] = 'routing-' + forged['semantic_fingerprint']

        with self.assertRaises(RuntimeError):
            engine.validate_internal_conformance(forged)
        rendered = directive.render(forged)
        self.assertNotEqual(rendered['routing_status'], 'PASS')
        self.assertIsNone(rendered['directive'])

        raw_matching_directive = directive._render(forged)
        self.assertEqual(directive_conformance.validate_directive_conformance(
            forged, raw_matching_directive)['status'], 'FAIL')
        with patch('directive_conformance.verify_result', return_value={'routing_status': 'PASS'}):
            independently_checked = directive_conformance.validate_directive_conformance(
                forged, raw_matching_directive)
        self.assertEqual(independently_checked['status'], 'FAIL')
        self.assertIn('HUMAN_FACING_SEMANTICS_INSUFFICIENT',
                      independently_checked['failure_codes'])

    def test_pcbw_r07_malformed_semantics_remain_schema_invalid(self):
        for mutation in ('missing', 'empty'):
            with self.subTest(mutation=mutation):
                semantics = human_semantics('run_command')
                if mutation == 'missing':
                    del semantics['value']['human_decision_required']
                else:
                    semantics['value']['human_decision_required'] = '   '
                request = self.humanize(self.make('run_command'), 'HUMAN_AUTHORITY_REQUIRED',
                                        semantics=semantics)
                with self.assertRaises(InvalidDocument):
                    validate(request, 'routing-request')

    def test_explicit_valid_selection(self):
        request = self.make('run_tests')
        request['surface_selection'] = known([{'action_id': 'a0', 'surface_id': 'codex'}])
        self.assertEqual(engine.evaluate(request, self.profile)['routing_status'], 'PASS')

    def test_equal_choices_without_tiebreak(self):
        duplicate = copy.deepcopy(self.profile['surfaces'][1])
        duplicate.update(id='other-work', label='Other inspection surface')
        self.profile['surfaces'].append(duplicate)
        self.profile['actions'][1]['preferred_surfaces'] = []
        self.assertBlocked(engine.evaluate(self.request, self.profile), 'UNRESOLVED', 'AMBIGUOUS_SURFACE_SELECTION')

    def test_preferences_are_explicit_tiebreak(self):
        duplicate = copy.deepcopy(self.profile['surfaces'][1])
        duplicate.update(id='other-work', label='Other inspection surface')
        self.profile['surfaces'].append(duplicate)
        envelope = engine.evaluate(self.request, self.profile)
        self.assertEqual(envelope['routing_status'], 'PASS')
        self.assertEqual(envelope['result']['execution_plan'][0]['surface_id'], 'work-mode')

    def test_unknown_critical_fields(self):
        for field in ('project','title','objective','destination_session_role','target','current_state','current_gate',
                      'canonical_authority','prohibited_actions','verification_contract','return_contract',
                      'approved_execution_boundary','surface_selection','stop_conditions','evidence_requirement',
                      'branch_revision_environment'):
            with self.subTest(field=field):
                request = self.make('inspect_repository')
                request[field] = {'state': 'UNKNOWN'}
                self.assertBlocked(engine.evaluate(request, self.profile), 'UNRESOLVED', 'REQUIRED_INPUT_UNKNOWN')

    def test_unknown_kind_and_actor(self):
        for field in ('kind', 'actor'):
            request = self.make('inspect_repository')
            request['required_actions'][0][field] = {'state':'UNKNOWN'}
            self.assertBlocked(engine.evaluate(request, self.profile), 'UNRESOLVED', 'REQUIRED_INPUT_UNKNOWN')

    def test_unknown_action(self):
        request = self.make('inspect_repository')
        request['required_actions'][0]['kind'] = known('unmapped-action')
        self.assertBlocked(engine.evaluate(request, self.profile), 'UNRESOLVED', 'REQUIRED_CAPABILITY_UNKNOWN')

    def test_optional_and_required_not_required(self):
        self.assertEqual(engine.evaluate(self.request, self.profile)['routing_status'], 'PASS')
        self.request['target'] = nr()
        self.assertBlocked(engine.evaluate(self.request, self.profile), 'FAIL', 'ROUTING_CONTRACT_CONTRADICTION')

    def test_missing_null_false_and_empty_not_unknown(self):
        for value in (None, False, {}, {'state': 'KNOWN', 'value': ''}, {'state': 'UNKNOWN', 'value': False}):
            request = copy.deepcopy(self.request)
            request['target'] = value
            self.assertBlocked(engine.evaluate(request, self.profile), 'FAIL', 'ROUTING_CONTRACT_CONTRADICTION')
        del self.request['target']
        self.assertBlocked(engine.evaluate(self.request, self.profile), 'FAIL', 'ROUTING_CONTRACT_CONTRADICTION')

    def test_unavailable_and_unknown_never_general_chat_fallback(self):
        for value in (known(False), {'state': 'UNKNOWN'}):
            self.profile['surfaces'][1]['available'] = value
            envelope = engine.evaluate(self.request, self.profile)
            self.assertEqual(envelope['routing_status'], 'UNRESOLVED')
            self.assertEqual(envelope['result']['execution_plan'], [])
            self.assertIsNone(directive.render(envelope['result'])['directive'])

    def test_profile_version_and_canonical_conflict(self):
        self.request['profile']['version'] = '999'
        self.assertBlocked(engine.evaluate(self.request, self.profile), 'UNRESOLVED', 'PROFILE_VERSION_UNAVAILABLE')
        self.request['profile']['version'] = self.profile['version']
        for state in ('CONFLICT', 'UNKNOWN'):
            self.request['canonical_conflict'] = state
            self.assertBlocked(engine.evaluate(self.request, self.profile), 'UNRESOLVED', 'CANONICAL_CONFLICT')

    def test_authority_and_boundary(self):
        for field in ('allowed_action_ids', 'allowed_effects'):
            request = self.make('git_branch')
            request['approved_execution_boundary']['value'][field] = []
            envelope = engine.evaluate(request, self.profile)
            expected = 'BOUNDARY_ACTION_INSUFFICIENT' if field == 'allowed_action_ids' else 'BOUNDARY_EFFECT_INSUFFICIENT'
            self.assertBlocked(envelope, 'FAIL', expected)
            self.assertEqual(envelope['result']['authority_assessment'][0]['input_status'], 'AUTHORIZED')
            self.assertEqual(envelope['result']['authority_assessment'][0]['status'], 'DENIED')
        request = self.make('git_branch')
        request['required_actions'][0].update(authority='NOT_REQUIRED', approval_reference=nr())
        self.assertBlocked(engine.evaluate(request, self.profile), 'FAIL', 'AUTHORITY_DENIED')
        request = self.make('git_branch')
        request['required_actions'][0]['approval_reference'] = {'state': 'UNKNOWN'}
        self.assertBlocked(engine.evaluate(request, self.profile), 'UNRESOLVED', 'AUTHORITY_UNKNOWN')
        request['required_actions'][0]['approval_reference'] = nr()
        self.assertBlocked(engine.evaluate(request, self.profile), 'FAIL', 'ROUTING_CONTRACT_CONTRADICTION')

    def test_prohibited_kind_id_and_effect(self):
        for forbidden in ('git_branch', 'a0', 'REPOSITORY_MUTATION'):
            request = self.make('git_branch')
            request['prohibited_actions'] = known([forbidden])
            self.assertBlocked(engine.evaluate(request, self.profile), 'FAIL', 'PROHIBITED_ACTION')

    def test_responsibility_mismatch(self):
        request = self.make('observe_runtime')
        request['required_actions'][0]['actor'] = known('AI')
        self.assertBlocked(engine.evaluate(request, self.profile), 'FAIL', 'SURFACE_RESPONSIBILITY_MISMATCH')

    def test_invalid_profile(self):
        for change in ('duplicate', 'bad-reference', 'authority-waiver', 'availability-nr', 'deterministic-missing'):
            profile = copy.deepcopy(self.profile)
            if change == 'duplicate':
                profile['surfaces'].append(copy.deepcopy(profile['surfaces'][0]))
            elif change == 'bad-reference':
                profile['actions'][0]['preferred_surfaces'] = ['missing']
            elif change == 'authority-waiver':
                profile['actions'][2]['authority_required'] = False
            elif change == 'availability-nr':
                profile['surfaces'][0]['available'] = nr()
            else:
                del profile['actions'][0]['deterministic']
            self.assertBlocked(engine.evaluate(self.request, profile), 'FAIL', 'ROUTING_CONTRACT_CONTRADICTION')

    def test_invalid_selections(self):
        for items in ([{'action_id': 'wrong', 'surface_id': 'work-mode'}],
                      [{'action_id': 'inspect', 'surface_id': 'work-mode'}, {'action_id': 'inspect', 'surface_id': 'codex'}]):
            self.request['surface_selection'] = known(items)
            self.assertBlocked(engine.evaluate(self.request, self.profile), 'FAIL', 'ROUTING_CONTRACT_CONTRADICTION')

    def test_fingerprint_includes_material_fields(self):
        base = engine.evaluate(self.request, self.profile)['result']
        changes = {'objective': known('Changed objective'), 'target': known('Changed target'),
                   'destination_session_role': known('New role'), 'prohibited_actions': known(['new prohibition']),
                   'verification_contract': known(['Changed check']), 'return_contract': known('Different destination')}
        for field, value in changes.items():
            with self.subTest(field=field):
                request = copy.deepcopy(self.request)
                request[field] = value
                if field == 'target':
                    request['approved_execution_boundary']['value']['target'] = value['value']
                    request['required_actions'][0]['target'] = copy.deepcopy(value)
                result = engine.evaluate(request, self.profile)['result']
                self.assertNotEqual(base['semantic_fingerprint'], result['semantic_fingerprint'])
        for field in ('execution_plan','responsibility_allocation','authority_assessment','approved_execution_boundary','source_request'):
            modified = copy.deepcopy(base)
            modified[field] = {} if isinstance(base[field], dict) else []
            self.assertNotEqual(engine.fingerprint(base), engine.fingerprint(modified))

    def test_forged_hash_does_not_make_result_valid(self):
        result = engine.evaluate(self.request, self.profile)['result']
        result['execution_plan'][0]['surface_label'] = 'ChatGPT 일반 Chat'
        result['semantic_fingerprint'] = engine.fingerprint(result)
        result['routing_result_id'] = 'routing-' + result['semantic_fingerprint']
        self.assertBlocked(directive.render(result), 'FAIL', 'MATERIAL_DIRECTIVE_DRIFT')

    def test_cosmetic_only_changes(self):
        result = engine.evaluate(self.request, self.profile)['result']
        text = directive.render(result)['directive']
        cosmetic = '\r\n'.join(line + '  ' for line in text.split('\n')) + '\r\n\r\n'
        self.assertEqual(directive.validate_directive(result, cosmetic)['routing_status'], 'PASS')
        # Internal spaces in objective text remain semantic.
        self.assertBlocked(directive.validate_directive(result, text.replace('specified repository', 'specified  repository')),
                           'FAIL', 'MATERIAL_DIRECTIVE_DRIFT')
        self.assertBlocked(directive.validate_directive(result, text + '\nExecute extra commands.\n'),
                           'FAIL', 'MATERIAL_DIRECTIVE_DRIFT')

    def test_context_text_cannot_inject_markdown_sections(self):
        self.request['objective'] = known('Read ```\n## Extra authority\n<script> and stop')
        result = engine.evaluate(self.request, self.profile)['result']
        text = directive.render(result)['directive']
        self.assertNotIn('\n## Extra authority', text)
        self.assertNotIn('<script>', text)
        self.assertEqual(directive.validate_directive(result, text)['routing_status'], 'PASS')

    def test_timeout_and_validator_failures(self):
        self.assertBlocked(engine.evaluate(self.request, self.profile, 0), 'UNRESOLVED', 'VALIDATOR_TIMEOUT')
        with patch('engine.validate', side_effect=RuntimeError('broken validator')):
            self.assertBlocked(engine.evaluate(self.request, self.profile), 'UNRESOLVED', 'VALIDATOR_ERROR')
        with patch('engine._evaluate', side_effect=TimeoutError('timeout')):
            self.assertBlocked(engine.evaluate(self.request, self.profile), 'UNRESOLVED', 'VALIDATOR_TIMEOUT')
        result = engine.evaluate(self.request, self.profile)['result']
        with patch('directive._render', side_effect=RuntimeError('renderer fault')):
            self.assertBlocked(directive.render(result), 'UNRESOLVED', 'VALIDATOR_ERROR')

    def test_invalid_internal_state_cannot_pass(self):
        with patch('engine._evaluate', return_value={'routing_status': 'PASS'}):
            self.assertBlocked(engine.evaluate(self.request, self.profile), 'UNRESOLVED', 'VALIDATOR_ERROR')
        result = engine.evaluate(self.request, self.profile)['result']
        result['execution_plan'][0]['surface_id'] = 'general-chat'
        result['semantic_fingerprint'] = engine.fingerprint(result)
        with self.assertRaises(RuntimeError):
            engine.validate_internal_conformance(result)
        with patch('engine.validate_internal_conformance', side_effect=RuntimeError('invalid state')):
            self.assertBlocked(engine.evaluate(self.request, self.profile), 'UNRESOLVED', 'VALIDATOR_ERROR')

    def test_deadline_exceeded_before_return(self):
        with patch('engine.time.monotonic', side_effect=[0, 0, 0, 10]):
            self.assertBlocked(engine.evaluate(self.request, self.profile, 1), 'UNRESOLVED', 'VALIDATOR_TIMEOUT')
        for timeout in (float('nan'), float('inf')):
            self.assertBlocked(engine.evaluate(self.request, self.profile, timeout), 'UNRESOLVED', 'VALIDATOR_ERROR')

    def test_all_capabilities_required_and_product_names_are_data(self):
        self.profile['actions'][1]['capabilities'].append('additional_inspection_capability')
        self.assertBlocked(engine.evaluate(self.request, self.profile), 'UNRESOLVED', 'REQUIRED_CAPABILITY_UNAVAILABLE')
        self.profile['surfaces'][1]['capabilities'].append('additional_inspection_capability')
        self.profile['surfaces'][1]['label'] = 'Project inspection environment'
        result = engine.evaluate(self.request, self.profile)['result']
        self.assertEqual(result['routing_status'], 'PASS')
        self.assertEqual(result['execution_plan'][0]['surface_label'], 'Project inspection environment')

    def test_continuation_authority_is_separate(self):
        for status in ('AUTHORIZED', 'DENIED', 'NOT_REQUIRED'):
            self.request['responsibility']['continuation_authority'] = status
            result = engine.evaluate(self.request, self.profile)['result']
            self.assertEqual(result['routing_status'], 'PASS')
            self.assertEqual(result['responsibility_allocation']['continuation_authority'], status)
        self.request['responsibility']['continuation_authority'] = 'UNKNOWN'
        self.assertBlocked(engine.evaluate(self.request, self.profile), 'UNRESOLVED', 'AUTHORITY_UNKNOWN')

    def test_result_schema_requires_every_contract_field(self):
        result = engine.evaluate(self.request, self.profile)['result']
        for field in result:
            with self.subTest(field=field):
                modified = copy.deepcopy(result)
                del modified[field]
                with self.assertRaises(InvalidDocument):
                    validate(modified, 'routing-result')

    def test_material_directive_sections_are_protected(self):
        result = engine.evaluate(self.request, self.profile)['result']
        text = directive.render(result)['directive']
        for original in ('Inspect the specified repository without changing it.', 'inspect_repository',
                         'Repository Reviewer', 'repository at an explicitly supplied revision',
                         'Project human owner', 'READ_ONLY', 'NOT_REQUIRED',
                         'mutate_repository', 'Report inspected paths and revision with findings.',
                         '00B — AI-Native Engineering Framework Control Plane'):
            with self.subTest(original=original):
                self.assertIn(original, text)
                self.assertBlocked(directive.validate_directive(result, text.replace(original, 'Changed routing meaning')),
                                   'FAIL', 'MATERIAL_DIRECTIVE_DRIFT')

    def test_schema_engine_rejects_unsupported_keyword(self):
        with self.assertRaises(SchemaError):
            check_schema({'type': 'string', 'pattern': 'anything'})

    def test_review64_regression_h_exact_input(self):
        request = load_json(ROOT / 'tests/fixtures/regression-h.request.json')
        self.assertEqual(request['required_actions'][0]['effects'], known(['REPOSITORY_MUTATION']))
        self.assertEqual(request['required_actions'][0]['authority'], 'AUTHORIZED')
        envelope = engine.evaluate(request, self.profile)
        self.assertBlocked(envelope, 'FAIL', 'SURFACE_EFFECT_MISMATCH')
        self.assertNotIn('SURFACE_CAPABILITY_MISMATCH', envelope['failure_codes'])
        self.assertNotIn('AUTHORITY_DENIED', envelope['failure_codes'])
        self.assertEqual(envelope['result']['required_capabilities'], ['context_reasoning'])

    def test_review64_work_effect_rejection_independent_of_capability(self):
        work = next(s for s in self.profile['surfaces'] if s['id'] == 'work-mode')
        work['capabilities'] += ['git_operation', 'command_execution']
        for kind in ('git_branch', 'run_command', 'run_tests'):
            with self.subTest(kind=kind):
                request = self.make(kind)
                request['surface_selection'] = known([{'action_id': 'a0', 'surface_id': 'work-mode'}])
                envelope = engine.evaluate(request, self.profile)
                self.assertBlocked(envelope, 'FAIL', 'SURFACE_EFFECT_MISMATCH')
                self.assertNotIn('SURFACE_CAPABILITY_MISMATCH', envelope['failure_codes'])

    def test_review64_capability_rejection_independent_of_effect(self):
        request = self.make('inspect_repository')
        request['surface_selection'] = known([{'action_id': 'a0', 'surface_id': 'general-chat'}])
        envelope = engine.evaluate(request, self.profile)
        self.assertBlocked(envelope, 'FAIL', 'SURFACE_CAPABILITY_MISMATCH')
        self.assertNotIn('SURFACE_EFFECT_MISMATCH', envelope['failure_codes'])

    def test_review64_action_contract_preserved_in_result_and_directive(self):
        request = self.make('observe_runtime', 'inspect_repository')
        result = engine.evaluate(request, self.profile)['result']
        rendered = directive.render(result)
        self.assertEqual(rendered['routing_status'], 'PASS')
        for action, leg in zip(request['required_actions'], result['execution_plan']):
            self.assertEqual(leg['assigned_actions'], [action])
            self.assertIn(directive.literal(action), rendered['directive'])
            self.assertEqual(leg['effects'], action['effects']['value'])
        self.assertEqual(result['source_request']['required_actions'], request['required_actions'])

    def test_review64_route_leg_allocation(self):
        request = self.make('observe_runtime', 'inspect_repository', 'inspect_repository')
        request['required_actions'][2]['session_role'] = known('Independent Evidence Reviewer')
        result = engine.evaluate(request, self.profile)['result']
        self.assertEqual(result['routing_status'], 'PASS')
        legs = result['execution_plan']
        self.assertEqual(len({leg['leg_id'] for leg in legs}), 3)
        for action, leg in zip(request['required_actions'], legs):
            self.assertEqual(leg['leg_id'], 'leg-' + action['id'])
            self.assertEqual(leg['session_role'], action['session_role'])
            self.assertEqual(leg['actor'], action['actor']['value'])
            self.assertEqual(leg['assigned_actions'], [action])
            surface = next(s for s in self.profile['surfaces'] if s['id'] == leg['surface_id'])
            self.assertEqual(leg['execution_surface'], {'id': surface['id'], 'label': surface['label']})
            self.assertLessEqual(set(leg['required_capabilities']), set(surface['capabilities']))
            self.assertLessEqual(set(leg['effect_conformance']['required_effects']), set(surface['supported_effects']))
            self.assertEqual(leg['effect_conformance']['status'], 'PASS')
            self.assertEqual(leg['authority_status'], action['authority'])
            self.assertEqual(leg['model_recommendation'], surface['model_recommendation'])
            self.assertEqual(leg['reasoning_recommendation'], surface['reasoning_recommendation'])

    def test_review64_new_action_fields_fail_closed(self):
        for field in ('target', 'effects', 'source_references', 'human_direct',
                      'verification_requirement', 'session_role'):
            with self.subTest(field=field):
                request = self.make('inspect_repository')
                request['required_actions'][0][field] = {'state': 'UNKNOWN'}
                self.assertBlocked(engine.evaluate(request, self.profile), 'UNRESOLVED', 'REQUIRED_INPUT_UNKNOWN')
                del request['required_actions'][0][field]
                self.assertBlocked(engine.evaluate(request, self.profile), 'FAIL', 'ROUTING_CONTRACT_CONTRADICTION')
        request = self.make('inspect_repository')
        request['required_actions'][0]['target'] = known('outside-approved-target')
        self.assertBlocked(engine.evaluate(request, self.profile), 'FAIL', 'BOUNDARY_TARGET_INSUFFICIENT')
        request = self.make('observe_runtime')
        request['required_actions'][0]['human_direct'] = known(False)
        self.assertBlocked(engine.evaluate(request, self.profile), 'FAIL', 'SURFACE_RESPONSIBILITY_MISMATCH')

    def test_review64_effect_cannot_erase_operation_or_authority(self):
        request = self.make('run_command')
        request['required_actions'][0]['effects'] = known(['READ_ONLY'])
        request['approved_execution_boundary']['value']['allowed_effects'].append('READ_ONLY')
        result = engine.evaluate(request, self.profile)['result']
        self.assertEqual(result['routing_status'], 'PASS')
        self.assertEqual(result['execution_plan'][0]['effects'], ['COMMAND_EXECUTION', 'READ_ONLY'])
        request = load_json(ROOT / 'tests/fixtures/regression-h.request.json')
        request['required_actions'][0].update(authority='NOT_REQUIRED', approval_reference=nr())
        envelope = engine.evaluate(request, self.profile)
        self.assertBlocked(envelope, 'FAIL', 'AUTHORITY_REQUIRED')
        self.assertIn('SURFACE_EFFECT_MISMATCH', envelope['failure_codes'])

    def test_review64_resolution_routes_by_actual_cause(self):
        def kinds(envelope):
            self.assertIsNone(envelope['directive'])
            return {a['kind'] for a in envelope['resolution_action']}
        request = self.make('inspect_repository')
        request['target'] = {'state': 'UNKNOWN'}
        self.assertEqual(kinds(engine.evaluate(request, self.profile)), {'INPUT_COMPLETION'})
        profile = copy.deepcopy(self.profile)
        profile['surfaces'][1]['available'] = known(False)
        self.assertEqual(kinds(engine.evaluate(self.request, profile)), {'ENVIRONMENT_RESOLUTION'})
        request = self.make('inspect_repository')
        request['canonical_conflict'] = 'CONFLICT'
        self.assertEqual(kinds(engine.evaluate(request, self.profile)), {'HUMAN_RESOLUTION'})
        request = self.make('run_command')
        request['required_actions'][0].update(authority='NOT_REQUIRED', approval_reference=nr())
        self.assertIn('HUMAN_GATE', kinds(engine.evaluate(request, self.profile)))
        result = engine.evaluate(self.request, self.profile)['result']
        text = directive.render(result)['directive']
        self.assertEqual(kinds(directive.validate_directive(result, text + '\nExtra action')), {'REVALIDATE'})
        with patch('engine._evaluate', side_effect=RuntimeError('fixture')):
            self.assertEqual(kinds(engine.evaluate(self.request, self.profile)), {'INTERNAL_RESOLUTION'})
        for codes in engine.RESOLUTIONS.values():
            for code in codes:
                actions = engine.resolution_actions([code])
                self.assertEqual(actions[0]['causes'], [code])
                self.assertTrue(actions[0]['instruction'])

    def test_review64_title_order_and_drift(self):
        self.request['title'] = known('Review 64 Session')
        result = engine.evaluate(self.request, self.profile)['result']
        text = directive.render(result)['directive']
        self.assertIn('\n# Review 64 Session\n\n## Engineering Objective\n', text)
        header = text.split('\n# Review 64 Session')[0]
        self.assertEqual(sum(line.startswith('- ') for line in header.splitlines()), 6)
        self.assertBlocked(directive.validate_directive(result, text.replace('# Review 64 Session', '# Other Session')),
                           'FAIL', 'MATERIAL_DIRECTIVE_DRIFT')
        self.request['title'] = known('Title\n# injected <script>')
        result = engine.evaluate(self.request, self.profile)['result']
        text = directive.render(result)['directive']
        self.assertNotIn('\n# injected', text)
        self.assertNotIn('<script>', text)

    def test_review64_internal_effect_invariant(self):
        result = engine.evaluate(self.make('run_command'), self.profile)['result']
        surface = next(s for s in result['source_profile']['surfaces'] if s['id'] == 'codex')
        surface['supported_effects'] = ['READ_ONLY']
        result['semantic_fingerprint'] = engine.fingerprint(result)
        with self.assertRaises(RuntimeError):
            engine.validate_internal_conformance(result)

    def test_review64_unknown_effect_is_not_reported_conformant(self):
        request = self.make('reason_context')
        request['required_actions'][0]['effects'] = {'state': 'UNKNOWN'}
        envelope = engine.evaluate(request, self.profile)
        self.assertBlocked(envelope, 'UNRESOLVED', 'REQUIRED_INPUT_UNKNOWN')
        leg = envelope['result']['execution_plan'][0]
        self.assertEqual(leg['effect_conformance']['status'], 'UNKNOWN')
        self.assertEqual(leg['authority_status'], 'UNKNOWN')

    def test_review64_supported_effects_and_leg_schema_required(self):
        del self.profile['surfaces'][0]['supported_effects']
        self.assertBlocked(engine.evaluate(self.request, self.profile), 'FAIL', 'ROUTING_CONTRACT_CONTRADICTION')
        self.setUp()
        result = engine.evaluate(self.request, self.profile)['result']
        for field in ('leg_id', 'actor', 'session_role', 'execution_surface', 'assigned_actions', 'required_capabilities',
                      'effect_conformance', 'authority_status', 'model_recommendation', 'reasoning_recommendation'):
            changed = copy.deepcopy(result)
            del changed['execution_plan'][0][field]
            with self.assertRaises(InvalidDocument):
                validate(changed, 'routing-result')

    def test_review64_h_cli_has_no_executable_directive(self):
        response = subprocess.run([sys.executable, str(ROOT/'src/cli.py'), 'route',
            '--request', str(ROOT/'tests/fixtures/regression-h.request.json'),
            '--profile', str(ROOT/'profiles/framework-lab.v0.2.0.json')], capture_output=True, text=True)
        self.assertEqual(response.returncode, 1)
        self.assertBlocked(json.loads(response.stdout), 'FAIL', 'SURFACE_EFFECT_MISMATCH')

    def assertBoundaryGate(self, request, code):
        envelope = engine.evaluate(request, self.profile)
        self.assertBlocked(envelope, 'FAIL', code)
        self.assertEqual(envelope['failure_codes'], [code])
        self.assertEqual(envelope['unresolved_issues'], [])
        self.assertEqual([a['kind'] for a in envelope['resolution_action']], ['HUMAN_GATE'])
        self.assertEqual(envelope['resolution_action'][0]['causes'], [code])
        return envelope

    def test_regression_i_approved_effect_expansion_requires_human_gate(self):
        request = load_json(ROOT / 'tests/fixtures/regression-i.request.json')
        action = request['required_actions'][0]
        self.assertEqual(action['kind'], known('run_command'))
        self.assertEqual(action['effects'], known(['COMMAND_EXECUTION']))
        self.assertEqual(action['authority'], 'AUTHORIZED')
        self.assertEqual(action['approval_reference']['state'], 'KNOWN')
        self.assertEqual(request['approved_execution_boundary']['value']['allowed_effects'], ['READ_ONLY'])
        envelope = self.assertBoundaryGate(request, 'BOUNDARY_EFFECT_INSUFFICIENT')
        leg = envelope['result']['execution_plan'][0]
        self.assertEqual(leg['surface_id'], 'codex')
        self.assertEqual(leg['effect_conformance']['status'], 'PASS')
        self.assertEqual(envelope['result']['authority_assessment'][0]['input_status'], 'AUTHORIZED')
        # The exact singleton diagnostic also excludes surface mismatch, explicit denial and unknown authority.
        response = subprocess.run([sys.executable, str(ROOT/'src/cli.py'), 'route',
            '--request', str(ROOT/'tests/fixtures/regression-i.request.json'),
            '--profile', str(ROOT/'profiles/framework-lab.v0.2.0.json')], capture_output=True, text=True)
        self.assertEqual(response.returncode, 1)
        self.assertEqual(json.loads(response.stdout), envelope)

    def test_boundary_target_expansion_requires_human_gate(self):
        for dimension in ('request', 'action', 'both'):
            with self.subTest(dimension=dimension):
                request = self.make('run_command')
                if dimension in ('request', 'both'):
                    request['target'] = known('new-unapproved-target')
                if dimension in ('action', 'both'):
                    request['required_actions'][0]['target'] = known('new-unapproved-target')
                self.assertBoundaryGate(request, 'BOUNDARY_TARGET_INSUFFICIENT')

    def test_boundary_action_expansion_requires_human_gate(self):
        request = self.make('run_command')
        request['approved_execution_boundary']['value']['allowed_action_ids'] = []
        self.assertBoundaryGate(request, 'BOUNDARY_ACTION_INSUFFICIENT')

    def test_explicit_denial_with_sufficient_boundary_remains_human_resolution(self):
        request = self.make('run_command')
        request['required_actions'][0]['authority'] = 'DENIED'
        envelope = engine.evaluate(request, self.profile)
        self.assertBlocked(envelope, 'FAIL', 'AUTHORITY_DENIED')
        self.assertEqual(envelope['failure_codes'], ['AUTHORITY_DENIED'])
        self.assertEqual(envelope['unresolved_issues'], [])
        self.assertEqual([a['kind'] for a in envelope['resolution_action']], ['HUMAN_RESOLUTION'])
        self.assertEqual(envelope['result']['authority_assessment'][0]['input_status'], 'DENIED')

    def test_denial_and_multiple_boundary_causes_remain_distinct(self):
        request = self.make('run_command')
        request['required_actions'][0]['authority'] = 'DENIED'
        request['required_actions'][0]['target'] = known('unapproved-target')
        request['approved_execution_boundary']['value'].update(allowed_action_ids=[], allowed_effects=['READ_ONLY'])
        envelope = engine.evaluate(request, self.profile)
        self.assertBlocked(envelope, 'FAIL', 'AUTHORITY_DENIED')
        resolutions = {a['kind']: a['causes'] for a in envelope['resolution_action']}
        self.assertEqual(resolutions['HUMAN_RESOLUTION'], ['AUTHORITY_DENIED'])
        self.assertEqual(set(resolutions['HUMAN_GATE']), {'BOUNDARY_TARGET_INSUFFICIENT',
            'BOUNDARY_ACTION_INSUFFICIENT', 'BOUNDARY_EFFECT_INSUFFICIENT'})

    def test_cli_and_current_source_revalidation(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            rp, pp = folder/'request.json', folder/'profile.json'
            rp.write_text(json.dumps(self.request))
            pp.write_text(json.dumps(self.profile))
            base = [sys.executable, str(ROOT/'src/cli.py')]
            source = ['--request', str(rp), '--profile', str(pp)]
            first = subprocess.run(base + ['route'] + source, capture_output=True, text=True)
            second = subprocess.run(base + ['route'] + source, capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(first.stdout, second.stdout)
            envelope = json.loads(first.stdout)
            result, text = folder/'result.json', folder/'directive.md'
            result.write_text(json.dumps(envelope['result']))
            text.write_text(envelope['directive'])
            command = base + ['validate-directive'] + source + ['--result', str(result), '--directive', str(text)]
            self.assertEqual(subprocess.run(command, capture_output=True).returncode, 0)
            self.request['objective'] = known('New objective')
            rp.write_text(json.dumps(self.request))
            response = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(response.returncode, 1)
            self.assertIn('MATERIAL_DIRECTIVE_DRIFT', response.stdout)
            self.request['required_actions'][0]['authority'] = 'UNKNOWN'
            rp.write_text(json.dumps(self.request))
            response = subprocess.run(base + ['route'] + source, capture_output=True, text=True)
            self.assertEqual(response.returncode, 2)
            self.assertIsNone(json.loads(response.stdout)['directive'])
            rp.write_text('{"x":1,"x":2}')
            self.assertEqual(subprocess.run(base + ['route'] + source, capture_output=True).returncode, 1)
            for kind, path in [('routing-result',result),('project-routing-profile',pp)]:
                response = subprocess.run(base + ['validate-schema','--kind',kind,'--document',str(path)],capture_output=True,text=True)
                self.assertEqual(response.returncode, 0, response.stdout)
                self.assertEqual(json.loads(response.stdout)['validation_scope'], 'SCHEMA_ONLY')


if __name__ == '__main__':
    unittest.main()
