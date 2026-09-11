import sys
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))

from semantic_sufficiency import (  # noqa: E402
    human_facing_semantics_issues,
    is_descriptive_operational_text,
    is_operational_interface,
    object_bearing_tokens,
)
from schema_validation import load_json  # noqa: E402


class SemanticSufficiencyTests(unittest.TestCase):
    def test_identifier_delimiter_variants_have_no_object_content(self):
        variants = (
            'FS 07 check', 'FS_07 state', 'fs-07 result',
            'C 0 state', 'C_0 result', 'C-0 check',
            'Step 3 result value', 'Step_3 result',
            'Phase A state result', 'Phase-A status',
        )
        for value in variants:
            with self.subTest(value=value):
                self.assertEqual(object_bearing_tokens(value), ())
                self.assertFalse(is_descriptive_operational_text(value))

    def test_status_placeholder_and_meta_compositions_are_not_descriptive(self):
        variants = (
            'Gate PASS now result', 'Gate-PASS state',
            'PASS value state', '[PASS] result', 'FAIL state', 'UNKNOWN value',
            'KNOWN status', 'NOT_REQUIRED result', 'NOT-REQUIRED state',
            'NOT REQUIRED value', 'TODO result', 'TBD state', 'N/A value',
        )
        for value in variants:
            with self.subTest(value=value):
                self.assertFalse(is_descriptive_operational_text(value))

    def test_full_practical_bypass_reports_every_semantic_field(self):
        semantics = load_json(ROOT / 'tests/fixtures/combined-control-meta-human-semantics.json')
        self.assertEqual(human_facing_semantics_issues(semantics), (
            'goal', 'primary_operational_interface', 'what_to_observe',
            'human_decision_required', 'expected_interpretation',
        ))

    def test_operational_descriptions_support_korean_english_and_mixed_text(self):
        values = (
            'Kafka consumer lag가 fault 종료 후 0으로 회복되는지 확인한다.',
            'Redis PEL에 pending entry가 남아 있는지 확인한다.',
            'consumer lag 확인',
            'database persistence resumed successfully',
        )
        for value in values:
            with self.subTest(value=value):
                self.assertTrue(is_descriptive_operational_text(value))

    def test_interface_rule_allows_names_but_rejects_control_compositions(self):
        for value in ('Grafana', 'Terminal', 'RedisInsight', 'MySQL Workbench', 'Kafka UI'):
            with self.subTest(valid=value):
                self.assertTrue(is_operational_interface(value))
        for value in ('C0 state', 'FS-07 result', '00C state', 'Gate status',
                      'PASS value', 'NOT_REQUIRED', 'Step 3', 'Phase A'):
            with self.subTest(invalid=value):
                self.assertFalse(is_operational_interface(value))


if __name__ == '__main__':
    unittest.main()
