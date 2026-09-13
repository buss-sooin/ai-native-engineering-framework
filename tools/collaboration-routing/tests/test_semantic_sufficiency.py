import copy
import sys
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))

from semantic_sufficiency import (  # noqa: E402
    human_facing_semantics_issues,
    is_supplemental_note,
    resolve_human_execution_responsibility,
    resolve_interface,
)
from schema_validation import load_json  # noqa: E402


def known(value):
    return {'state': 'KNOWN', 'value': value}


def nr():
    return {'state': 'NOT_REQUIRED'}


PROFILE = load_json(ROOT / 'profiles/framework-lab.v0.4.0.json')


def context(kind='run_command', capabilities=None):
    return {
        'profile': PROFILE,
        'action_id': 'a0',
        'action_kind': kind,
        'action_target': known('repository at an explicitly supplied revision'),
        'capabilities': capabilities or ['command_execution'],
        'verification_requirement': known(['Inspect repository runtime evidence.']),
        'human_necessity_basis': known('HUMAN_AUTHORITY_REQUIRED'),
        'human_return_responsibility': known({
            'kind': 'DECISION_OR_APPROVAL',
            'description': 'Approve or reject execution using the action-specific evidence and authority.',
            'source_references': ['framework-lab:human-authority'],
        }),
        'selected_surface_id': 'human-terminal',
    }


def structured(interface_id='human-terminal', source='SELECTED_EXECUTION_SURFACE',
               fallback='redis-cli'):
    return known({
        'action_id': 'a0',
        'target_reference': 'ACTION_TARGET',
        'interface_reference': {'source': source, 'id': interface_id},
        'observation': {
            'target_reference': 'ACTION_TARGET',
            'capability_ids': ['command_execution'],
            'verification_reference': 'ACTION_VERIFICATION_REQUIREMENT',
        },
        'decision_criterion_reference': 'ACTION_HUMAN_RETURN_RESPONSIBILITY',
        'interpretation_reference': 'PROFILE_ACTION_HUMAN_HANDOFF',
        'cli_fallback': (known({'source': 'PROFILE_OPERATIONAL_INTERFACE', 'id': fallback})
                         if fallback else nr()),
    })


def semantics(bindings=None, note='Additional operator context.'):
    return known({
        'structured_operational_semantics': structured() if bindings is None else bindings,
        'supplemental_note': known(note) if note is not None else nr(),
    })


class SemanticSufficiencyTests(unittest.TestCase):
    def test_selected_surface_resolves_from_profile_not_request_display_text(self):
        resolved = resolve_interface(
            {'source': 'SELECTED_EXECUTION_SURFACE', 'id': 'human-terminal'}, context())
        self.assertEqual(resolved, {
            'source': 'SELECTED_EXECUTION_SURFACE',
            'id': 'human-terminal',
            'display_name': 'Human IDE / Terminal',
            'surface_id': 'human-terminal',
        })
        self.assertIsNone(resolve_interface(
            {'source': 'SELECTED_EXECUTION_SURFACE', 'id': 'codex'}, context()))

    def test_named_interface_requires_profile_surface_and_capability_binding(self):
        runtime = context('observe_runtime', ['runtime_observation'])
        self.assertEqual(resolve_interface(
            {'source': 'PROFILE_OPERATIONAL_INTERFACE', 'id': 'grafana'}, runtime
        )['display_name'], 'Grafana')
        self.assertIsNone(resolve_interface(
            {'source': 'PROFILE_OPERATIONAL_INTERFACE', 'id': 'banana'}, runtime))

        wrong_surface = copy.deepcopy(runtime)
        wrong_surface['selected_surface_id'] = 'codex'
        self.assertIsNone(resolve_interface(
            {'source': 'PROFILE_OPERATIONAL_INTERFACE', 'id': 'grafana'}, wrong_surface))
        self.assertIsNone(resolve_interface(
            {'source': 'PROFILE_OPERATIONAL_INTERFACE', 'id': 'grafana'}, context()))

    def test_all_structured_bindings_are_cross_checked(self):
        self.assertEqual(human_facing_semantics_issues(semantics(), context()), ())
        mutations = (
            lambda value: value.update(action_id='other'),
            lambda value: value.update(target_reference='OTHER'),
            lambda value: value['interface_reference'].update(id='missing'),
            lambda value: value['observation'].update(capability_ids=['other']),
            lambda value: value['observation'].update(verification_reference='OTHER'),
            lambda value: value.update(decision_criterion_reference='OTHER'),
            lambda value: value.update(interpretation_reference='OTHER'),
            lambda value: value['cli_fallback']['value'].update(id='missing'),
        )
        for mutate in mutations:
            with self.subTest(mutate=mutate):
                supplied = semantics()
                mutate(supplied['value']['structured_operational_semantics']['value'])
                self.assertTrue(human_facing_semantics_issues(supplied, context()))

    def test_arbitrary_supplemental_vocabulary_has_zero_pass_authority(self):
        for word in ('review', 'report', 'assessment', 'summary', 'inspection',
                     'analysis', 'evaluation', 'operation', 'activity', 'banana', 'foobar'):
            with self.subTest(word=word):
                self.assertTrue(is_supplemental_note(word))
                invalid = semantics(bindings={'state': 'UNKNOWN'}, note=word)
                self.assertIn('structured_operational_semantics',
                              human_facing_semantics_issues(invalid, context()))

    def test_legacy_free_text_shapes_are_never_sufficient(self):
        for fixture in ('identifier-only-human-semantics.json',
                        'combined-control-meta-human-semantics.json',
                        'review-report-human-semantics.json'):
            with self.subTest(fixture=fixture):
                supplied = load_json(ROOT / 'tests/fixtures' / fixture)
                self.assertIn('human_facing_semantics',
                              human_facing_semantics_issues(supplied, context()))

    def test_korean_prefix_terms_are_allowed_as_supplemental_notes(self):
        for value in ('작업자 queue 확인', '실행기 로그 확인',
                      '상태머신 오류 확인', '관측기 metric 확인'):
            with self.subTest(value=value):
                self.assertEqual(
                    human_facing_semantics_issues(semantics(note=value), context()), ())

    def test_resolved_handoff_ignores_supplemental_note_for_required_meaning(self):
        action = {
            'id': 'a0', 'target': context()['action_target'],
            'verification_requirement': context()['verification_requirement'],
            'human_necessity_basis': known('HUMAN_AUTHORITY_REQUIRED'),
            'human_return_responsibility': context()['human_return_responsibility'],
            'human_facing_semantics': semantics(note='banana'),
        }
        step = {'kind': 'run_command', 'surface_id': 'human-terminal',
                'required_capabilities': ['command_execution']}
        resolved = resolve_human_execution_responsibility(action, step, PROFILE)
        self.assertNotEqual(resolved['Human Goal'], 'banana')
        self.assertEqual(resolved['Primary Operational Interface / Tool']['display_name'],
                         'Human IDE / Terminal')
        self.assertEqual(resolved['CLI / low-level fallback']['value']['display_name'],
                         'redis-cli')
        self.assertEqual(resolved['Supplemental Human Note'], known('banana'))


if __name__ == '__main__':
    unittest.main()
