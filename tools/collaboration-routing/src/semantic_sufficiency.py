"""Deterministic minimum-content checks for PCBW-R07 Human-facing semantics.

The classifier establishes a bounded lower limit. It removes known workflow,
status, placeholder and generic meta/action vocabulary, then requires content
that can name an operational subject or object. It does not judge prose quality
or attempt unrestricted natural-language understanding.
"""
import re


HUMAN_NECESSITY_BASES = frozenset({
    'HUMAN_AUTHORITY_REQUIRED',
    'DIRECT_HUMAN_OBSERVATION_OBJECTIVE',
    'HUMAN_RISK_CONTROL_REQUIRED',
    'HUMAN_LEARNING_OBJECTIVE',
    'HUMAN_EXECUTION_SIMPLER_OR_SAFER',
    'NO_SUITABLE_AUTHORIZED_AI_SURFACE',
})

_STATUS_TERMS = frozenset({
    'pass', 'passed', 'fail', 'failed', 'unresolved', 'known', 'unknown',
    'not', 'not-required', 'not_required', 'required', 'ok', 'done', 'complete', 'completed',
})
_PLACEHOLDER_TERMS = frozenset({
    'todo', 'tbd', 'n/a', 'na', 'none', 'null', 'placeholder', 'test',
    'sample', 'example', 'dummy', 'temp', 'temporary',
})
_CONTROL_TERMS = frozenset({
    'gate', 'phase', 'step', 'stage', 'cohort', 'control', 'checkpoint',
    'section', 'scenario',
})
_GENERIC_META_ACTION_TERMS = frozenset({
    'check', 'checks', 'checked', 'checking', 'state', 'states', 'status',
    'result', 'results', 'value', 'values', 'decision', 'decisions',
    'condition', 'conditions', 'item', 'items', 'case', 'cases',
    'run', 'runs', 'running', 'ran', 'action', 'actions', 'process', 'processes',
    'current', 'currently', 'now', 'next', 'previous', 'expected', 'actual',
    'perform', 'performs', 'performed', 'execute', 'executes', 'executed',
    'execution', 'observe', 'observes', 'observed', 'verify', 'verifies',
    'verified', 'verification', 'decide', 'decides', 'decided',
    'human', 'goal', 'responsibility', 'requested', 'approved', 'boundary',
    'primary', 'operational', 'interface', 'tool', 'fallback', 'command',
    'use', 'uses', 'used', 'using', 'only', 'when', 'then', 'with', 'without',
    'direct', 'named', 'return', 'returns', 'conforming', 'insufficient',
    'information', 'data', 'detail', 'details',
})
_KOREAN_NON_OBJECT_STEMS = (
    '확인', '판단', '결정', '관측', '관찰', '검증', '실행', '수행',
    '상태', '결과', '값', '조건', '단계', '항목', '사례', '작업',
    '현재', '다음', '이전', '예상', '실제', '요청', '승인', '필요',
    '책임', '목표', '완료', '통과', '진입', '미정', '없음', '해당없음',
    '플레이스홀더', '테스트', '임시',
)
_NON_OBJECT_TERMS = frozenset().union(
    _STATUS_TERMS,
    _PLACEHOLDER_TERMS,
    _CONTROL_TERMS,
    _GENERIC_META_ACTION_TERMS,
)
_INTERNAL_IDENTIFIER_PREFIXES = frozenset({
    'fs', 'c', 'gate', 'phase', 'step', 'stage', 'control', 'checkpoint',
    'section', 'scenario', 'case',
})
_TOKEN = re.compile(r'[0-9A-Za-z가-힣]+')
_COMPACT_INTERNAL_IDENTIFIER = re.compile(r'^(?:[A-Za-z]{1,12}\d+|\d{2}[A-Za-z])$')


def _tokens(value):
    if not isinstance(value, str):
        return []
    return _TOKEN.findall(value.strip())


def _internal_identifier_fragment_indexes(tokens):
    """Recognize compact and delimiter-fragmented workflow/control identifiers."""
    indexes = set()
    for index, token in enumerate(tokens):
        if _COMPACT_INTERNAL_IDENTIFIER.fullmatch(token):
            indexes.add(index)
        if index + 1 >= len(tokens):
            continue
        following = tokens[index + 1]
        prefix = token.casefold()
        uppercase_label = token.isascii() and token.isalpha() and token.isupper()
        suffix_like = following.isdigit() or len(following) == 1
        if suffix_like and (prefix in _INTERNAL_IDENTIFIER_PREFIXES or uppercase_label):
            indexes.update((index, index + 1))
    return indexes


def _is_object_bearing_token(token, internal_identifier_fragment=False):
    normalized = token.casefold()
    return (not internal_identifier_fragment
            and not re.fullmatch(r'\d+[가-힣]*', token)
            and normalized not in _NON_OBJECT_TERMS
            and not any(normalized.startswith(stem) for stem in _KOREAN_NON_OBJECT_STEMS)
            and len(token) > 1)


def object_bearing_tokens(value):
    """Return candidate operational subject/object tokens after normalization."""
    tokens = _tokens(value)
    internal = _internal_identifier_fragment_indexes(tokens)
    return tuple(token for index, token in enumerate(tokens)
                 if _is_object_bearing_token(token, index in internal))


def is_descriptive_operational_text(value):
    """Require object-bearing content, not only IDs/control/meta/placeholders."""
    objects = object_bearing_tokens(value)
    return len(objects) >= 2 and sum(map(len, objects)) >= 6


def is_operational_interface(value):
    """Allow concise tool names while rejecting IDs and control-only labels."""
    return bool(object_bearing_tokens(value))


def human_facing_semantics_issues(semantics):
    """Return the Human-facing fields that fail the deterministic minimum contract."""
    if not isinstance(semantics, dict) or semantics.get('state') != 'KNOWN':
        return ('human_facing_semantics',)
    value = semantics.get('value')
    if not isinstance(value, dict):
        return ('human_facing_semantics',)

    issues = []
    if not is_descriptive_operational_text(value.get('goal')):
        issues.append('goal')
    if not is_operational_interface(value.get('primary_operational_interface')):
        issues.append('primary_operational_interface')

    observations = value.get('what_to_observe')
    if (not isinstance(observations, list) or not observations
            or any(not is_descriptive_operational_text(item) for item in observations)):
        issues.append('what_to_observe')
    if not is_descriptive_operational_text(value.get('human_decision_required')):
        issues.append('human_decision_required')
    if not is_descriptive_operational_text(value.get('expected_interpretation')):
        issues.append('expected_interpretation')

    fallback = value.get('cli_fallback')
    if not isinstance(fallback, dict) or fallback.get('state') not in ('KNOWN', 'NOT_REQUIRED'):
        issues.append('cli_fallback')
    elif (fallback.get('state') == 'KNOWN'
          and not is_descriptive_operational_text(fallback.get('value'))):
        issues.append('cli_fallback')
    return tuple(issues)


def human_execution_projection_issues(responsibilities):
    """Validate the rendered Human Execution Responsibility projection directly."""
    if not isinstance(responsibilities, list) or not responsibilities:
        return ('Human Execution Responsibility',)
    issues = []
    for index, item in enumerate(responsibilities):
        prefix = 'Human Execution Responsibility[' + str(index) + '].'
        if not isinstance(item, dict):
            issues.append(prefix.rstrip('.'))
            continue
        if item.get('Human Necessity Basis') not in HUMAN_NECESSITY_BASES:
            issues.append(prefix + 'Human Necessity Basis')
        semantics = {
            'state': 'KNOWN',
            'value': {
                'goal': item.get('Human Goal'),
                'primary_operational_interface': item.get('Primary Operational Interface / Tool'),
                'what_to_observe': item.get('What to Observe'),
                'human_decision_required': item.get('Human Decision Required'),
                'expected_interpretation': item.get('Expected Interpretation'),
                'cli_fallback': item.get('CLI / low-level fallback'),
            },
        }
        issues.extend(prefix + field for field in human_facing_semantics_issues(semantics))
    return tuple(issues)
