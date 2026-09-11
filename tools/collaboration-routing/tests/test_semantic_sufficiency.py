import copy
import sys
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))

from semantic_sufficiency import (  # noqa: E402
    human_facing_semantics_issues,
    is_applicable_human_text,
    is_operational_interface,
)
from schema_validation import load_json  # noqa: E402


def known(value):
    return {'state': 'KNOWN', 'value': value}


def nr():
    return {'state': 'NOT_REQUIRED'}


def context():
    return {
        'action_id': 'a0',
        'action_target': known('repository at an explicitly supplied revision'),
        'capabilities': ['command_execution'],
        'verification_requirement': known(['Inspect repository runtime evidence.']),
        'selected_surface_id': 'human-terminal',
        'selected_surface_label': 'Human IDE / Terminal',
        'verification_contract': known(['Report repository runtime evidence.']),
    }


def structured(interface='Human IDE / Terminal', interface_id='human-terminal',
               interface_kind='SELECTED_EXECUTION_SURFACE'):
    return known({
        'action_id': 'a0',
        'target_reference': 'ACTION_TARGET',
        'interface': {
            'kind': interface_kind,
            'id': interface_id,
            'display_name': interface,
            'surface_id': 'human-terminal',
        },
        'observation': {
            'target_reference': 'ACTION_TARGET',
            'capability_ids': ['command_execution'],
            'verification_reference': 'ACTION_VERIFICATION_REQUIREMENT',
        },
        'decision_criterion_reference': 'ACTION_VERIFICATION_REQUIREMENT',
        'interpretation_reference': 'REQUEST_VERIFICATION_CONTRACT',
        'cli_fallback': nr(),
    })


def semantics(interface='Human IDE / Terminal', bindings=None):
    return known({
        'goal': 'Inspect repository runtime evidence for recovery.',
        'primary_operational_interface': interface,
        'what_to_observe': ['Kafka consumer lag and Redis pending entries.'],
        'human_decision_required': 'Determine whether database persistence recovered.',
        'expected_interpretation': 'Persisted records establish recovery completion.',
        'cli_fallback': nr(),
        'structured_operational_semantics': structured() if bindings is None else bindings,
    })


class SemanticSufficiencyTests(unittest.TestCase):
    def test_free_text_is_not_positive_structured_evidence(self):
        for word in ('review', 'report', 'assessment', 'summary', 'inspection',
                     'analysis', 'evaluation', 'operation', 'activity'):
            with self.subTest(word=word):
                supplied = semantics(bindings={'state': 'UNKNOWN'})
                supplied['value']['goal'] = 'FS-07 ' + word
                supplied['value']['what_to_observe'] = ['Gate PASS ' + word]
                supplied['value']['human_decision_required'] = 'Step 3 ' + word
                supplied['value']['expected_interpretation'] = 'PASS ' + word
                self.assertIn('structured_operational_semantics',
                              human_facing_semantics_issues(supplied, context()))

    def test_positive_structured_bindings_are_required_and_cross_checked(self):
        self.assertEqual(human_facing_semantics_issues(semantics(), context()), ())
        mutations = (
            ('action_id', lambda value: value.update(action_id='other')),
            ('target', lambda value: value.update(target_reference='OTHER')),
            ('capability', lambda value: value['observation'].update(capability_ids=['other'])),
            ('verification', lambda value: value['observation'].update(verification_reference='OTHER')),
            ('decision', lambda value: value.update(decision_criterion_reference='OTHER')),
            ('interpretation', lambda value: value.update(interpretation_reference='OTHER')),
            ('surface', lambda value: value['interface'].update(surface_id='other')),
        )
        for label, mutate in mutations:
            with self.subTest(label=label):
                supplied = semantics()
                mutate(supplied['value']['structured_operational_semantics']['value'])
                self.assertTrue(human_facing_semantics_issues(supplied, context()))

    def test_known_exploit_fixtures_fail_for_missing_positive_structure(self):
        fixtures = (
            'identifier-only-human-semantics.json',
            'combined-control-meta-human-semantics.json',
            'review-report-human-semantics.json',
        )
        for fixture in fixtures:
            with self.subTest(fixture=fixture):
                supplied = load_json(ROOT / 'tests/fixtures' / fixture)
                self.assertIn('structured_operational_semantics',
                              human_facing_semantics_issues(supplied, context()))

    def test_korean_prefix_technical_nouns_are_not_rejected(self):
        values = ('작업자 queue 확인', '실행기 로그 확인', '상태머신 오류 확인', '관측기 metric 확인')
        for value in values:
            with self.subTest(value=value):
                supplied = semantics()
                supplied['value']['goal'] = value
                self.assertEqual(human_facing_semantics_issues(supplied, context()), ())
                self.assertTrue(is_applicable_human_text(value))

    def test_mixed_language_operational_text_remains_applicable(self):
        values = (
            'Kafka consumer lag가 0으로 회복됐는지 확인한다.',
            'Redis PEL에 pending entry가 남아 있는지 확인한다.',
            'consumer lag 확인',
            'database persistence resumed successfully',
        )
        for value in values:
            with self.subTest(value=value):
                self.assertTrue(is_applicable_human_text(value))

    def test_named_interfaces_are_open_but_control_mixtures_are_rejected(self):
        valid = ('Grafana', 'Terminal', 'RedisInsight', 'MySQL Workbench',
                 'Kafka UI', 'IntelliJ IDEA', 'psql', 'redis-cli')
        invalid = ('C0 review', 'FS-07 console', 'Gate tool', 'PASS terminal')
        for value in valid:
            with self.subTest(valid=value):
                self.assertTrue(is_operational_interface(value))
                supplied = semantics(
                    value, structured(value, value.casefold().replace(' ', '-'),
                                      'NAMED_OPERATIONAL_INTERFACE'))
                self.assertEqual(human_facing_semantics_issues(supplied, context()), ())
        for value in invalid:
            with self.subTest(invalid=value):
                self.assertFalse(is_operational_interface(value))

    def test_old_human_semantics_shape_is_not_sufficient(self):
        supplied = semantics()
        del supplied['value']['structured_operational_semantics']
        self.assertIn('structured_operational_semantics',
                      human_facing_semantics_issues(supplied, context()))


if __name__ == '__main__':
    unittest.main()
