"""Deterministic minimum-content checks for PCBW-R07 Human-facing semantics."""
import re


HUMAN_NECESSITY_BASES = frozenset({
    'HUMAN_AUTHORITY_REQUIRED',
    'DIRECT_HUMAN_OBSERVATION_OBJECTIVE',
    'HUMAN_RISK_CONTROL_REQUIRED',
    'HUMAN_LEARNING_OBJECTIVE',
    'HUMAN_EXECUTION_SIMPLER_OR_SAFER',
    'NO_SUITABLE_AUTHORIZED_AI_SURFACE',
})

_CONTROL_OR_PLACEHOLDER_TERMS = frozenset({
    'pass', 'passed', 'fail', 'failed', 'unresolved', 'unknown',
    'todo', 'tbd', 'n/a', 'na', 'none', 'null', 'placeholder', 'test',
    'ok', 'done', 'complete', 'completed',
    'gate', 'phase', 'step', 'stage', 'cohort', 'control', 'checkpoint',
    '확인', '진입', '통과', '완료', '미정', '없음', '해당없음',
    '플레이스홀더', '테스트', '임시',
})
_TOKEN = re.compile(r'[0-9A-Za-z가-힣]+(?:-[0-9A-Za-z가-힣]+)*')
_INTERNAL_IDENTIFIER = re.compile(
    r'^(?:[A-Z]{1,12}(?:-[A-Z0-9]+)+|[A-Z]{1,4}\d+|\d{2}[A-Z])$'
)


def _tokens(value):
    if not isinstance(value, str):
        return []
    return _TOKEN.findall(value.strip())


def _is_internal_identifier(token):
    return bool(_INTERNAL_IDENTIFIER.fullmatch(token.upper()))


def _is_meaningful_token(token):
    normalized = token.casefold()
    return (normalized not in _CONTROL_OR_PLACEHOLDER_TERMS
            and not _is_internal_identifier(token)
            and len(token) > 1)


def is_descriptive_operational_text(value):
    """Require bounded descriptive content, not only IDs/control/placeholders."""
    meaningful = [token for token in _tokens(value) if _is_meaningful_token(token)]
    return len(meaningful) >= 2 and sum(map(len, meaningful)) >= 6


def is_operational_interface(value):
    """Allow concise tool names while rejecting IDs and control-only labels."""
    tokens = _tokens(value)
    return bool(tokens) and any(_is_meaningful_token(token) for token in tokens)


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
