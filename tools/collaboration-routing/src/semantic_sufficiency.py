"""Positive structured conformance for PCBW-R07 Human-facing semantics.

Free text remains presentation material. PASS authority comes from bindings to
the action target, profile capabilities, selected surface, action verification
requirements and request verification contract. Bounded lexical checks only
reject obvious placeholders, formal statuses and workflow identifiers.
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

_FORMAL_STATUS_TERMS = frozenset({
    'pass', 'passed', 'fail', 'failed', 'unresolved', 'known', 'unknown',
    'not', 'required', 'ok', 'done', 'complete', 'completed',
})
_PLACEHOLDER_TERMS = frozenset({
    'todo', 'tbd', 'n', 'a', 'na', 'none', 'null', 'placeholder', 'test',
    'sample', 'example', 'dummy', 'temp', 'temporary',
    '미정', '없음', '해당없음', '플레이스홀더', '테스트', '임시',
})
_CONTROL_TERMS = frozenset({
    'gate', 'phase', 'step', 'stage', 'control', 'checkpoint',
    'section', 'scenario', 'case', 'state', 'status', 'result', 'value',
    '확인', '판단', '결정', '관측', '관찰', '검증', '실행', '수행',
    '작업', '상태', '결과', '조건', '단계', '항목', '사례',
})
_INTERNAL_IDENTIFIER_PREFIXES = frozenset({
    'fs', 'c', 'gate', 'phase', 'step', 'stage', 'control', 'checkpoint',
    'section', 'scenario', 'case',
})
_TOKEN = re.compile(r'[0-9A-Za-z가-힣]+')
_COMPACT_INTERNAL_IDENTIFIER = re.compile(r'^(?:[A-Za-z]{1,12}\d+|\d{2}[A-Za-z])$')
_MACHINE_ID = re.compile(r'^[A-Za-z0-9][A-Za-z0-9._-]*$')


def _tokens(value):
    if not isinstance(value, str):
        return []
    return _TOKEN.findall(value.strip())


def _internal_identifier_fragment_indexes(tokens):
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


def _obvious_non_semantic_indexes(tokens):
    internal = _internal_identifier_fragment_indexes(tokens)
    return internal | {
        index for index, token in enumerate(tokens)
        if re.fullmatch(r'\d+[가-힣]*', token)
        or token.casefold() in _FORMAL_STATUS_TERMS
        or token.casefold() in _PLACEHOLDER_TERMS
        or token.casefold() in _CONTROL_TERMS
    }


def is_applicable_human_text(value):
    """Reject only obvious non-content; this is not positive PASS evidence."""
    tokens = _tokens(value)
    if not tokens:
        return False
    excluded = _obvious_non_semantic_indexes(tokens)
    return any(index not in excluded and len(token) > 1
               for index, token in enumerate(tokens))


def is_operational_interface(value):
    """Validate a named interface without using a product allowlist."""
    tokens = _tokens(value)
    if not tokens:
        return False
    excluded = _obvious_non_semantic_indexes(tokens)
    if excluded:
        return False
    return any(len(token) > 1 for token in tokens)


def _interface_issues(interface, prose, context, prefix):
    if not isinstance(interface, dict):
        return (prefix,)
    required = {'kind', 'id', 'display_name', 'surface_id'}
    if set(interface) != required:
        return (prefix,)
    kind = interface.get('kind')
    identifier = interface.get('id')
    display_name = interface.get('display_name')
    issues = []
    if kind not in ('NAMED_OPERATIONAL_INTERFACE', 'SELECTED_EXECUTION_SURFACE'):
        issues.append(prefix + '.kind')
    if (not isinstance(identifier, str) or not _MACHINE_ID.fullmatch(identifier)
            or not is_operational_interface(identifier)):
        issues.append(prefix + '.id')
    if not is_operational_interface(display_name):
        issues.append(prefix + '.display_name')
    if display_name != prose:
        issues.append(prefix + '.display_name_binding')
    if interface.get('surface_id') != context.get('selected_surface_id'):
        issues.append(prefix + '.surface_id')
    if kind == 'SELECTED_EXECUTION_SURFACE':
        if identifier != context.get('selected_surface_id'):
            issues.append(prefix + '.selected_surface_id')
        if display_name != context.get('selected_surface_label'):
            issues.append(prefix + '.selected_surface_label')
    return tuple(issues)


def _structured_issues(structured, prose, context):
    if not isinstance(structured, dict) or structured.get('state') != 'KNOWN':
        return ('structured_operational_semantics',)
    value = structured.get('value')
    required = {
        'action_id', 'target_reference', 'interface', 'observation',
        'decision_criterion_reference', 'interpretation_reference', 'cli_fallback',
    }
    if not isinstance(value, dict) or set(value) != required:
        return ('structured_operational_semantics',)

    issues = []
    if value.get('action_id') != context.get('action_id'):
        issues.append('structured_operational_semantics.action_id')
    if (value.get('target_reference') != 'ACTION_TARGET'
            or not isinstance(context.get('action_target'), dict)
            or context['action_target'].get('state') != 'KNOWN'):
        issues.append('structured_operational_semantics.target_reference')
    issues.extend(_interface_issues(
        value.get('interface'), prose.get('primary_operational_interface'), context,
        'structured_operational_semantics.interface'))

    observation = value.get('observation')
    if not isinstance(observation, dict) or set(observation) != {
            'target_reference', 'capability_ids', 'verification_reference'}:
        issues.append('structured_operational_semantics.observation')
    else:
        if observation.get('target_reference') != 'ACTION_TARGET':
            issues.append('structured_operational_semantics.observation.target_reference')
        capabilities = observation.get('capability_ids')
        if (not isinstance(capabilities, list)
                or sorted(capabilities) != sorted(context.get('capabilities', []))):
            issues.append('structured_operational_semantics.observation.capability_ids')
        if (observation.get('verification_reference') != 'ACTION_VERIFICATION_REQUIREMENT'
                or not isinstance(context.get('verification_requirement'), dict)
                or context['verification_requirement'].get('state') != 'KNOWN'
                or not context['verification_requirement'].get('value')):
            issues.append('structured_operational_semantics.observation.verification_reference')

    if value.get('decision_criterion_reference') != 'ACTION_VERIFICATION_REQUIREMENT':
        issues.append('structured_operational_semantics.decision_criterion_reference')
    verification_contract = context.get('verification_contract')
    if (value.get('interpretation_reference') != 'REQUEST_VERIFICATION_CONTRACT'
            or not isinstance(verification_contract, dict)
            or verification_contract.get('state') != 'KNOWN'
            or not verification_contract.get('value')):
        issues.append('structured_operational_semantics.interpretation_reference')

    fallback = value.get('cli_fallback')
    prose_fallback = prose.get('cli_fallback')
    if not isinstance(fallback, dict) or fallback.get('state') not in ('KNOWN', 'NOT_REQUIRED'):
        issues.append('structured_operational_semantics.cli_fallback')
    elif fallback.get('state') == 'NOT_REQUIRED':
        if fallback != {'state': 'NOT_REQUIRED'} or prose_fallback != {'state': 'NOT_REQUIRED'}:
            issues.append('structured_operational_semantics.cli_fallback')
    else:
        if (set(fallback) != {'state', 'value'} or not isinstance(prose_fallback, dict)
                or prose_fallback.get('state') != 'KNOWN'
                or not is_applicable_human_text(prose_fallback.get('value'))
                or not isinstance(fallback.get('value'), dict)):
            issues.append('structured_operational_semantics.cli_fallback')
        else:
            issues.extend(_interface_issues(
                fallback.get('value'), fallback['value'].get('display_name'), context,
                'structured_operational_semantics.cli_fallback.value'))
    return tuple(issues)


def human_facing_semantics_issues(semantics, context=None):
    """Return fields that fail presentation or positive structured conformance."""
    if not isinstance(semantics, dict) or semantics.get('state') != 'KNOWN':
        return ('human_facing_semantics',)
    value = semantics.get('value')
    if not isinstance(value, dict):
        return ('human_facing_semantics',)
    context = context or {}

    issues = []
    for field in ('goal', 'human_decision_required', 'expected_interpretation'):
        if not is_applicable_human_text(value.get(field)):
            issues.append(field)
    if not is_operational_interface(value.get('primary_operational_interface')):
        issues.append('primary_operational_interface')
    observations = value.get('what_to_observe')
    if (not isinstance(observations, list) or not observations
            or any(not is_applicable_human_text(item) for item in observations)):
        issues.append('what_to_observe')
    fallback = value.get('cli_fallback')
    if (not isinstance(fallback, dict) or fallback.get('state') not in ('KNOWN', 'NOT_REQUIRED')
            or (fallback.get('state') == 'KNOWN'
                and not is_applicable_human_text(fallback.get('value')))):
        issues.append('cli_fallback')
    issues.extend(_structured_issues(
        value.get('structured_operational_semantics'), value, context))
    return tuple(issues)


def resolved_operational_context(action, step, verification_contract):
    """Project a structured binding onto the actual validated routing context.

    This helper deliberately tolerates malformed/forged inputs so that every
    downstream validation boundary can fail closed instead of raising while it
    inspects an invalid PASS result.
    """
    semantics = action.get('human_facing_semantics', {}).get('value', {})
    structured = semantics.get('structured_operational_semantics')
    structured_value = (structured.get('value', {})
                        if isinstance(structured, dict) else {})
    if not isinstance(structured_value, dict):
        structured_value = {}
    return {
        'Action': {
            'id': action.get('id'),
            'kind': action.get('kind'),
            'target': action.get('target'),
        },
        'Interface': structured_value.get('interface'),
        'Observation': {
            'target': action.get('target'),
            'capabilities': step.get('required_capabilities'),
            'verification_requirement': action.get('verification_requirement'),
        },
        'Human Decision Criterion': action.get('verification_requirement'),
        'Expected Interpretation Contract': verification_contract,
        'CLI / low-level fallback': structured_value.get('cli_fallback'),
    }


def human_execution_projection_issues(responsibilities, execution_plan, verification_contract):
    """Validate rendered Human responsibilities against Routing Result structure."""
    if not isinstance(responsibilities, list) or not responsibilities:
        return ('Human Execution Responsibility',)
    human_steps = [step for step in execution_plan if step.get('actor') == 'HUMAN']
    if len(responsibilities) != len(human_steps):
        return ('Human Execution Responsibility',)

    issues = []
    for index, (item, step) in enumerate(zip(responsibilities, human_steps)):
        prefix = 'Human Execution Responsibility[' + str(index) + '].'
        if not isinstance(item, dict):
            issues.append(prefix.rstrip('.'))
            continue
        action = step['assigned_actions'][0]
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
                'structured_operational_semantics': item.get('Structured Operational Semantics'),
            },
        }
        context = {
            'action_id': action.get('id'),
            'action_target': action.get('target'),
            'capabilities': step.get('required_capabilities'),
            'verification_requirement': action.get('verification_requirement'),
            'selected_surface_id': step.get('surface_id'),
            'selected_surface_label': step.get('surface_label'),
            'verification_contract': verification_contract,
        }
        expected_resolved = resolved_operational_context(action, step, verification_contract)
        if item.get('Resolved Operational Context') != expected_resolved:
            issues.append(prefix + 'Resolved Operational Context')
        issues.extend(prefix + field for field in human_facing_semantics_issues(
            semantics, context))
    return tuple(issues)
