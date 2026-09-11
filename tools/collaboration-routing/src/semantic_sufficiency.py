"""Trusted structured conformance for PCBW-R07 Human handoffs.

Request prose is supplemental and never establishes PASS. Required Human-facing
responsibility is resolved from the selected action, Project Routing Profile,
selected surface, target, capabilities and verification bindings.
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

_PLACEHOLDER_VALUES = frozenset({
    '', 'todo', 'tbd', 'n/a', 'na', 'none', 'null', 'placeholder',
    '미정', '없음', '해당없음', '플레이스홀더',
})
_MACHINE_ID = re.compile(r'^[A-Za-z0-9][A-Za-z0-9._-]*$')


def is_supplemental_note(value):
    """Bounded defense for optional prose; this never supplies PASS authority."""
    return (isinstance(value, str)
            and value.strip().casefold() not in _PLACEHOLDER_VALUES)


def is_human_usable_description(value):
    """Reject opaque Profile labels without attempting natural-language scoring."""
    if not isinstance(value, str):
        return False
    text = value.strip()
    return len(text) >= 12 and len(text.split()) >= 2 and not _MACHINE_ID.fullmatch(text)


def _profile_maps(profile):
    if not isinstance(profile, dict):
        return {}, {}, {}
    return (
        {item.get('kind'): item for item in profile.get('actions', [])
         if isinstance(item, dict)},
        {item.get('id'): item for item in profile.get('surfaces', [])
         if isinstance(item, dict)},
        {item.get('id'): item for item in profile.get('operational_interfaces', [])
         if isinstance(item, dict)},
    )


def resolve_interface(reference, context):
    """Resolve an interface only from the selected surface or trusted Profile."""
    if not isinstance(reference, dict) or set(reference) != {'source', 'id'}:
        return None
    source = reference.get('source')
    identifier = reference.get('id')
    _, surfaces, interfaces = _profile_maps(context.get('profile'))
    selected_surface_id = context.get('selected_surface_id')
    capabilities = set(context.get('capabilities') or [])

    if source == 'SELECTED_EXECUTION_SURFACE':
        surface = surfaces.get(identifier)
        if (identifier != selected_surface_id or not surface
                or surface.get('actor') != 'HUMAN'):
            return None
        return {
            'source': source,
            'id': surface['id'],
            'display_name': surface['label'],
            'surface_id': surface['id'],
        }

    if source == 'PROFILE_OPERATIONAL_INTERFACE':
        interface = interfaces.get(identifier)
        if (not interface
                or selected_surface_id not in interface.get('compatible_surface_ids', [])
                or not capabilities <= set(interface.get('capability_ids', []))):
            return None
        return {
            'source': source,
            'id': interface['id'],
            'display_name': interface['display_name'],
            'surface_id': selected_surface_id,
        }
    return None


def _structured_issues(structured, context):
    if not isinstance(structured, dict) or structured.get('state') != 'KNOWN':
        return ('structured_operational_semantics',)
    value = structured.get('value')
    required = {
        'action_id', 'target_reference', 'interface_reference', 'observation',
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
    if resolve_interface(value.get('interface_reference'), context) is None:
        issues.append('structured_operational_semantics.interface_reference')

    observation = value.get('observation')
    if not isinstance(observation, dict) or set(observation) != {
            'target_reference', 'capability_ids', 'verification_reference'}:
        issues.append('structured_operational_semantics.observation')
    else:
        if observation.get('target_reference') != 'ACTION_TARGET':
            issues.append('structured_operational_semantics.observation.target_reference')
        capabilities = observation.get('capability_ids')
        if (not isinstance(capabilities, list)
                or sorted(capabilities) != sorted(context.get('capabilities') or [])):
            issues.append('structured_operational_semantics.observation.capability_ids')
        verification = context.get('verification_requirement')
        if (observation.get('verification_reference') != 'ACTION_VERIFICATION_REQUIREMENT'
                or not isinstance(verification, dict)
                or verification.get('state') != 'KNOWN'
                or not verification.get('value')):
            issues.append('structured_operational_semantics.observation.verification_reference')

    if value.get('decision_criterion_reference') != 'ACTION_VERIFICATION_REQUIREMENT':
        issues.append('structured_operational_semantics.decision_criterion_reference')
    if value.get('interpretation_reference') != 'PROFILE_ACTION_HUMAN_HANDOFF':
        issues.append('structured_operational_semantics.interpretation_reference')

    actions, _, _ = _profile_maps(context.get('profile'))
    definition = actions.get(context.get('action_kind'))
    handoff = definition.get('human_handoff') if isinstance(definition, dict) else None
    if (not isinstance(handoff, dict)
            or any(not is_human_usable_description(handoff.get(field))
                   for field in ('goal', 'observation', 'decision', 'expected_interpretation'))):
        issues.append('structured_operational_semantics.profile_human_handoff')

    fallback = value.get('cli_fallback')
    if fallback == {'state': 'NOT_REQUIRED'}:
        pass
    elif (not isinstance(fallback, dict) or set(fallback) != {'state', 'value'}
          or fallback.get('state') != 'KNOWN'
          or resolve_interface(fallback.get('value'), context) is None):
        issues.append('structured_operational_semantics.cli_fallback')
    return tuple(issues)


def human_facing_semantics_issues(semantics, context=None):
    """Return violations of the trusted Human responsibility contract."""
    if not isinstance(semantics, dict) or semantics.get('state') != 'KNOWN':
        return ('human_facing_semantics',)
    value = semantics.get('value')
    if not isinstance(value, dict) or set(value) != {
            'structured_operational_semantics', 'supplemental_note'}:
        return ('human_facing_semantics',)
    note = value.get('supplemental_note')
    if (not isinstance(note, dict) or note.get('state') not in ('KNOWN', 'NOT_REQUIRED')
            or (note.get('state') == 'KNOWN'
                and (set(note) != {'state', 'value'}
                     or not is_supplemental_note(note.get('value'))))
            or (note.get('state') == 'NOT_REQUIRED' and note != {'state': 'NOT_REQUIRED'})):
        return ('supplemental_note',)
    return _structured_issues(value.get('structured_operational_semantics'), context or {})


def resolve_human_execution_responsibility(action, step, profile):
    """Build required Human-facing meaning from trusted/resolved context only."""
    semantics = action['human_facing_semantics']['value']
    structured = semantics['structured_operational_semantics']['value']
    actions, _, _ = _profile_maps(profile)
    handoff = actions[step['kind']]['human_handoff']
    context = {
        'profile': profile,
        'action_id': action['id'],
        'action_kind': step['kind'],
        'action_target': action['target'],
        'capabilities': step['required_capabilities'],
        'verification_requirement': action['verification_requirement'],
        'selected_surface_id': step['surface_id'],
    }
    interface = resolve_interface(structured['interface_reference'], context)
    fallback = structured['cli_fallback']
    resolved_fallback = ({'state': 'NOT_REQUIRED'} if fallback['state'] == 'NOT_REQUIRED'
                         else {'state': 'KNOWN',
                               'value': resolve_interface(fallback['value'], context)})
    return {
        'Action ID': action['id'],
        'Human Goal': {
            'description': handoff['goal'],
            'action_kind': step['kind'],
            'target': action['target']['value'],
        },
        'Human Necessity Basis': action['human_necessity_basis']['value'],
        'Primary Operational Interface / Tool': interface,
        'What to Observe': {
            'description': handoff['observation'],
            'target': action['target']['value'],
            'capabilities': step['required_capabilities'],
            'verification_requirement': action['verification_requirement']['value'],
        },
        'Human Decision Required': {
            'description': handoff['decision'],
            'verification_requirement': action['verification_requirement']['value'],
        },
        'Expected Interpretation': {
            'description': handoff['expected_interpretation'],
        },
        'CLI / low-level fallback': resolved_fallback,
        'Supplemental Human Note': semantics['supplemental_note'],
        'Structured Operational Semantics': semantics['structured_operational_semantics'],
    }


def human_execution_projection_issues(responsibilities, execution_plan, profile):
    """Validate rendered Human responsibilities against trusted Profile context."""
    if not isinstance(responsibilities, list):
        return ('Human Execution Responsibility',)
    human_steps = [step for step in execution_plan if step.get('actor') == 'HUMAN']
    if len(responsibilities) != len(human_steps):
        return ('Human Execution Responsibility',)

    issues = []
    for index, (actual, step) in enumerate(zip(responsibilities, human_steps)):
        prefix = 'Human Execution Responsibility[' + str(index) + ']'
        if not isinstance(actual, dict):
            issues.append(prefix)
            continue
        action = step['assigned_actions'][0]
        context = {
            'profile': profile,
            'action_id': action.get('id'),
            'action_kind': step.get('kind'),
            'action_target': action.get('target'),
            'capabilities': step.get('required_capabilities'),
            'verification_requirement': action.get('verification_requirement'),
            'selected_surface_id': step.get('surface_id'),
        }
        semantic_issues = human_facing_semantics_issues(
            action.get('human_facing_semantics'), context)
        issues.extend(prefix + '.' + item for item in semantic_issues)
        if not semantic_issues:
            expected = resolve_human_execution_responsibility(action, step, profile)
            if actual != expected:
                issues.append(prefix + '.trusted_projection')
    return tuple(issues)
