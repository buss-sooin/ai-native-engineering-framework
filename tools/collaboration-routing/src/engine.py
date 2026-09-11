"""Transport-independent routing. No action execution or approval acquisition."""
import copy
import hashlib
import math
import time

from schema_validation import InvalidDocument, canonical, validate
from semantic_sufficiency import (
    HUMAN_NECESSITY_BASES,
    human_facing_semantics_issues,
    is_human_usable_description,
)

VERSION = '0.4.0'

RESOLUTIONS = {
    'INPUT_COMPLETION': ('REQUIRED_INPUT_UNKNOWN', 'REQUIRED_CAPABILITY_UNKNOWN', 'ROUTING_CONTRACT_CONTRADICTION',
                         'HUMAN_NECESSITY_BASIS_MISSING'),
    'ENVIRONMENT_RESOLUTION': ('REQUIRED_CAPABILITY_UNAVAILABLE', 'NO_FEASIBLE_SURFACE_AVAILABLE',
                               'PROFILE_VERSION_UNAVAILABLE', 'SURFACE_CAPABILITY_MISMATCH', 'SURFACE_EFFECT_MISMATCH'),
    'HUMAN_RESOLUTION': ('CANONICAL_CONFLICT', 'AMBIGUOUS_SURFACE_SELECTION', 'AUTHORITY_UNKNOWN',
                         'AUTHORITY_DENIED', 'PROHIBITED_ACTION', 'SURFACE_RESPONSIBILITY_MISMATCH',
                         'INVALID_HUMAN_DELEGATION', 'HUMAN_FACING_SEMANTICS_INSUFFICIENT',
                         'TARGETED_RE_EVALUATION_NOT_ESTABLISHED',
                         'NO_SUITABLE_AI_SURFACE_CONTRADICTION'),
    'HUMAN_GATE': ('AUTHORITY_REQUIRED', 'BOUNDARY_TARGET_INSUFFICIENT',
                   'BOUNDARY_ACTION_INSUFFICIENT', 'BOUNDARY_EFFECT_INSUFFICIENT'),
    'REVALIDATE': ('MATERIAL_DIRECTIVE_DRIFT', 'HEADER_BODY_MISMATCH'),
    'INTERNAL_RESOLUTION': ('VALIDATOR_ERROR', 'VALIDATOR_TIMEOUT'),
}

RESOLUTION_INSTRUCTIONS = {
    'INPUT_COMPLETION': 'Complete or correct structured input, then revalidate.',
    'ENVIRONMENT_RESOLUTION': 'Resolve profile, availability or capability/effect fit, then revalidate; do not lower requirements.',
    'HUMAN_RESOLUTION': 'Return the conflict or authority question to the responsible human; do not assume new permission.',
    'HUMAN_GATE': 'Obtain human approval covering the requested target, action and effects, or narrow the request to the approved boundary, then revalidate. Do not infer approval or override an explicit denial.',
    'REVALIDATE': 'Revalidate the changed contract and regenerate the directive; do not reuse the previous PASS.',
    'INTERNAL_RESOLUTION': 'Repair the validator or resolve its timeout, then rerun validation.',
}


def resolution_actions(codes):
    grouped = {}
    for code in sorted(set(codes)):
        kind = next((kind for kind, causes in RESOLUTIONS.items() if code in causes), 'INTERNAL_RESOLUTION')
        grouped.setdefault(kind, []).append(code)
    return [{'kind': kind, 'causes': grouped[kind], 'instruction': RESOLUTION_INSTRUCTIONS[kind]}
            for kind in RESOLUTIONS if kind in grouped]


class Deadline:
    def __init__(self, timeout_seconds):
        if not math.isfinite(timeout_seconds):
            raise ValueError('validation timeout must be finite')
        if timeout_seconds <= 0:
            raise TimeoutError('validation deadline expired')
        self.end = time.monotonic() + timeout_seconds

    def check(self):
        if time.monotonic() >= self.end:
            raise TimeoutError('validation deadline expired')


def fingerprint(result):
    content = {k: v for k, v in result.items() if k not in ('semantic_fingerprint', 'routing_result_id')}
    return hashlib.sha256(canonical(content).encode('utf-8')).hexdigest()


def unique_ids(items, key):
    values = [item[key] for item in items]
    if len(values) != len(set(values)):
        raise InvalidDocument('duplicate ' + key)


def validate_profile(profile):
    validate(profile, 'project-routing-profile')
    unique_ids(profile['actions'], 'kind')
    unique_ids(profile['surfaces'], 'id')
    unique_ids(profile['surfaces'], 'label')
    unique_ids(profile['operational_interfaces'], 'id')
    unique_ids(profile['operational_interfaces'], 'display_name')
    surface_ids = {s['id'] for s in profile['surfaces']}
    surfaces = {s['id']: s for s in profile['surfaces']}
    known_capabilities = {
        capability
        for item in profile['actions'] + profile['surfaces']
        for capability in item['capabilities']
    }
    for action in profile['actions']:
        if set(action['preferred_surfaces']) - surface_ids:
            raise InvalidDocument('preferred surface does not exist')
        # Project data cannot waive authorization for effects beyond read-only.
        if action['effects'] != ['READ_ONLY'] and not action['authority_required']:
            raise InvalidDocument('non-read-only effect requires authority')
        if any(not is_human_usable_description(action['human_handoff'][field])
               for field in ('goal', 'observation', 'decision', 'expected_interpretation')):
            raise InvalidDocument('action human handoff must contain usable trusted descriptions')
    for surface in profile['surfaces']:
        if surface['available']['state'] == 'NOT_REQUIRED':
            raise InvalidDocument('surface availability cannot be NOT_REQUIRED')
    for interface in profile['operational_interfaces']:
        if set(interface['compatible_surface_ids']) - surface_ids:
            raise InvalidDocument('operational interface surface does not exist')
        if any(surfaces[sid]['actor'] != 'HUMAN'
               for sid in interface['compatible_surface_ids']):
            raise InvalidDocument('operational interface requires Human-compatible surfaces')
        if set(interface['capability_ids']) - known_capabilities:
            raise InvalidDocument('operational interface capability does not exist')


def validate_internal_conformance(result):
    """Check PASS invariants independently of surface selection preferences."""
    validate(result, 'routing-result')
    if result['routing_status'] != 'PASS':
        return
    request, profile = result['source_request'], result['source_profile']
    required = {a['id']: a for a in request['required_actions']}
    definitions = {a['kind']: a for a in profile['actions']}
    surfaces = {s['id']: s for s in profile['surfaces']}
    plan = result['execution_plan']
    valid = not result['failure_codes'] and not result['unresolved_issues']
    valid = valid and len(plan) == len(required) and {s['action_id'] for s in plan} == set(required)
    for step in plan:
        action = required[step['action_id']]
        definition = definitions[action['kind']['value']]
        surface = surfaces[step['surface_id']]
        valid = valid and step['kind'] == action['kind']['value']
        valid = valid and step['actor'] == action['actor']['value'] == surface['actor']
        valid = valid and surface['available'] == {'state': 'KNOWN', 'value': True}
        valid = valid and set(step['capabilities']) == set(definition['capabilities'])
        valid = valid and set(step['capabilities']) <= set(surface['capabilities'])
        effects = set(definition['effects']) | set(action['effects']['value'])
        valid = valid and set(step['effects']) == effects
        valid = valid and effects <= set(surface['supported_effects'])
        valid = valid and step['assigned_actions'] == [action]
        valid = valid and step['leg_id'] == 'leg-' + action['id']
        valid = valid and step['session_role'] == action['session_role']
        valid = valid and step['execution_surface'] == {'id': surface['id'], 'label': surface['label']}
        valid = valid and step['required_capabilities'] == step['capabilities']
        valid = valid and step['effect_conformance'] == {'required_effects': sorted(effects),
            'supported_effects': sorted(surface['supported_effects']), 'status': 'PASS'}
        assessment = next(a for a in result['authority_assessment'] if a['action_id'] == action['id'])
        valid = valid and step['authority_status'] == assessment['status']
        valid = valid and step['authority_status'] in ('AUTHORIZED', 'NOT_REQUIRED')
        valid = valid and step['model_recommendation'] == surface['model_recommendation']
        valid = valid and step['reasoning_recommendation'] == surface['reasoning_recommendation']
        valid = valid and action['authority'] in ('AUTHORIZED', 'NOT_REQUIRED')
        valid = valid and (not (definition['authority_required'] or effects != {'READ_ONLY'}) or action['authority'] == 'AUTHORIZED')
        if step['actor'] == 'HUMAN':
            basis = action.get('human_necessity_basis', {'state': 'UNKNOWN'})
            semantics = action.get('human_facing_semantics', {'state': 'NOT_REQUIRED'})
            valid = valid and basis['state'] == 'KNOWN' and basis.get('value') in HUMAN_NECESSITY_BASES
            valid = valid and not human_facing_semantics_issues(semantics, {
                'profile': profile,
                'action_id': action['id'],
                'action_kind': step['kind'],
                'action_target': action['target'],
                'capabilities': step['required_capabilities'],
                'verification_requirement': action['verification_requirement'],
                'selected_surface_id': step['surface_id'],
                'selected_surface_label': step['surface_label'],
                'verification_contract': result['verification_contract'],
            })
            if basis.get('value') == 'NO_SUITABLE_AUTHORIZED_AI_SURFACE':
                reevaluation = action.get('targeted_re_evaluation_established', {'state': 'UNKNOWN'})
                valid = valid and reevaluation == {'state': 'KNOWN', 'value': True}
                valid = valid and not any(
                    candidate['actor'] == 'AI'
                    and set(definition['capabilities']) <= set(candidate['capabilities'])
                    and effects <= set(candidate['supported_effects'])
                    and candidate['available'] != {'state': 'KNOWN', 'value': False}
                    for candidate in surfaces.values())
        else:
            valid = valid and action.get('human_necessity_basis', {'state': 'NOT_REQUIRED'}) == {'state': 'NOT_REQUIRED'}
            valid = valid and action.get('targeted_re_evaluation_established', {'state': 'NOT_REQUIRED'}) == {'state': 'NOT_REQUIRED'}
            valid = valid and action.get('human_facing_semantics', {'state': 'NOT_REQUIRED'}) == {'state': 'NOT_REQUIRED'}
    valid = valid and result['semantic_fingerprint'] == fingerprint(result)
    if not valid:
        raise RuntimeError('internal PASS contract invariant failed')


def _evaluate(request, profile, deadline):
    validate(request, 'routing-request')
    validate_profile(profile)
    unique_ids(request['required_actions'], 'id')
    failures, issues = [], []

    def fail(code):
        if code not in failures:
            failures.append(code)

    def unresolved(code, detail):
        item = {'code': code, 'detail': detail}
        if item not in issues:
            issues.append(item)

    def needed(field, name, optional=False):
        if field['state'] == 'UNKNOWN':
            unresolved('REQUIRED_INPUT_UNKNOWN', name)
            return None
        if field['state'] == 'NOT_REQUIRED':
            if not optional:
                fail('ROUTING_CONTRACT_CONTRADICTION')
            return None
        return field['value']

    deadline.check()
    for name in ('project', 'title', 'objective', 'destination_session_role', 'target',
                 'current_state', 'current_gate', 'canonical_authority',
                 'prohibited_actions', 'verification_contract', 'return_contract'):
        needed(request[name], name)
    for name in ('stop_conditions', 'evidence_requirement', 'branch_revision_environment'):
        needed(request[name], name, optional=True)
    for name in ('decision_owner', 'verification_owner'):
        needed(request['responsibility'][name], name)
    if request['responsibility']['continuation_authority'] == 'UNKNOWN':
        unresolved('AUTHORITY_UNKNOWN', 'continuation_authority')
    if request['canonical_conflict'] != 'CLEAR':
        unresolved('CANONICAL_CONFLICT', 'canonical authority requires human resolution')
    if request['profile'] != {'id': profile['id'], 'version': profile['version']}:
        unresolved('PROFILE_VERSION_UNAVAILABLE', 'requested profile ID/version is unavailable')
    if request['project']['state'] == 'KNOWN' and request['project']['value'] != profile['project']:
        fail('ROUTING_CONTRACT_CONTRADICTION')

    actions = {a['kind']: a for a in profile['actions']}
    surfaces = {s['id']: s for s in profile['surfaces']}
    ids = {a['id'] for a in request['required_actions']}
    selection = needed(request['surface_selection'], 'surface_selection', optional=True)
    selected = {}
    if selection is not None:
        unique_ids(selection, 'action_id')
        selected = {s['action_id']: s['surface_id'] for s in selection}
        if set(selected) != ids:
            fail('ROUTING_CONTRACT_CONTRADICTION')
    boundary = needed(request['approved_execution_boundary'], 'approved_execution_boundary')
    target = request['target'].get('value')
    if boundary is not None:
        if target is not None and boundary['target'] != target:
            fail('BOUNDARY_TARGET_INSUFFICIENT')
        if set(boundary['allowed_action_ids']) - ids:
            fail('ROUTING_CONTRACT_CONTRADICTION')
    prohibited = request['prohibited_actions'].get('value', [])
    capabilities, feasible, plan, rejected, assessments = set(), [], [], [], []
    for required in request['required_actions']:
        deadline.check()
        aid = required['id']
        authority = required['authority']
        assessment = {'action_id': aid, 'input_status': authority, 'status': authority,
                      'approval_reference': copy.deepcopy(required['approval_reference'])}
        assessments.append(assessment)
        if authority != 'DENIED' and (boundary is None or target is None):
            assessment['status'] = 'UNKNOWN'
        if boundary is not None and target is not None and boundary['target'] != target:
            assessment['status'] = 'DENIED'
        if authority == 'UNKNOWN':
            unresolved('AUTHORITY_UNKNOWN', aid)
        elif authority == 'DENIED':
            fail('AUTHORITY_DENIED')
        elif authority == 'AUTHORIZED':
            ref = required['approval_reference']
            if ref['state'] == 'UNKNOWN':
                assessment['status'] = 'UNKNOWN' if assessment['status'] != 'DENIED' else 'DENIED'
                unresolved('AUTHORITY_UNKNOWN', aid + ': approval reference unknown')
            elif ref['state'] != 'KNOWN':
                assessment['status'] = 'DENIED'
                fail('ROUTING_CONTRACT_CONTRADICTION')
        elif required['approval_reference']['state'] != 'NOT_REQUIRED':
            fail('ROUTING_CONTRACT_CONTRADICTION')
        kind = needed(required['kind'], aid + '.kind')
        actor = needed(required['actor'], aid + '.actor')
        action_target = needed(required['target'], aid + '.target')
        declared_effects = needed(required['effects'], aid + '.effects')
        if declared_effects is None and assessment['status'] != 'DENIED':
            assessment['status'] = 'UNKNOWN'
        direct = needed(required['human_direct'], aid + '.human_direct')
        for field in ('source_references', 'verification_requirement', 'session_role'):
            needed(required[field], aid + '.' + field)
        if actor is not None and direct is not None and direct != (actor == 'HUMAN'):
            fail('SURFACE_RESPONSIBILITY_MISMATCH')
        if action_target is not None and boundary is not None and action_target != boundary['target']:
            fail('BOUNDARY_TARGET_INSUFFICIENT')
            assessment['status'] = 'DENIED'
        elif action_target is None and assessment['status'] != 'DENIED':
            assessment['status'] = 'UNKNOWN'
        if kind is None:
            unresolved('REQUIRED_CAPABILITY_UNKNOWN', aid)
            continue
        definition = actions.get(kind)
        if definition is None:
            unresolved('REQUIRED_CAPABILITY_UNKNOWN', kind)
            continue
        capabilities.update(definition['capabilities'])
        # Declared effects may add obligations, but cannot erase the operation's minimum effects.
        effects = set(definition['effects']) | set(declared_effects or [])
        if kind in prohibited or aid in prohibited or effects & set(prohibited):
            assessment['status'] = 'DENIED'
            fail('PROHIBITED_ACTION')
        if boundary is not None:
            if aid not in boundary['allowed_action_ids']:
                assessment['status'] = 'DENIED'
                fail('BOUNDARY_ACTION_INSUFFICIENT')
            if effects - set(boundary['allowed_effects']):
                assessment['status'] = 'DENIED'
                fail('BOUNDARY_EFFECT_INSUFFICIENT')
        if (definition['authority_required'] or effects != {'READ_ONLY'}) and authority == 'NOT_REQUIRED':
            assessment['status'] = 'DENIED'
            fail('AUTHORITY_DENIED')
            fail('AUTHORITY_REQUIRED')
        possible, unknown_available, suitable_ai, ai_suitability_unknown = [], False, [], False
        for sid in sorted(surfaces):
            surface = surfaces[sid]
            reasons = []
            if set(definition['capabilities']) - set(surface['capabilities']):
                reasons.append('SURFACE_CAPABILITY_MISMATCH')
            if effects - set(surface['supported_effects']):
                reasons.append('SURFACE_EFFECT_MISMATCH')
            if surface['actor'] != actor:
                reasons.append('SURFACE_RESPONSIBILITY_MISMATCH')
            if surface['available']['state'] == 'UNKNOWN':
                unknown_available = unknown_available or not reasons
                reasons.append('REQUIRED_INPUT_UNKNOWN')
            elif surface['available']['value'] is False:
                reasons.append('REQUIRED_CAPABILITY_UNAVAILABLE')
            if reasons:
                for reason in reasons:
                    rejected.append({'action_id': aid, 'surface_id': sid, 'reason': reason})
            else:
                possible.append(sid)
            if (surface['actor'] == 'AI'
                    and set(definition['capabilities']) <= set(surface['capabilities'])
                    and effects <= set(surface['supported_effects'])
                    and assessment['status'] in ('AUTHORIZED', 'NOT_REQUIRED')):
                if surface['available'] == {'state': 'KNOWN', 'value': True}:
                    suitable_ai.append(sid)
                elif surface['available']['state'] == 'UNKNOWN':
                    ai_suitability_unknown = True
        basis_field = required.get('human_necessity_basis',
                                   {'state': 'UNKNOWN'} if actor == 'HUMAN' else {'state': 'NOT_REQUIRED'})
        reevaluation_field = required.get('targeted_re_evaluation_established',
                                          {'state': 'UNKNOWN'} if actor == 'HUMAN' else {'state': 'NOT_REQUIRED'})
        semantics_field = required.get('human_facing_semantics', {'state': 'NOT_REQUIRED'})
        if actor == 'HUMAN':
            basis = basis_field.get('value') if basis_field['state'] == 'KNOWN' else None
            if basis is None:
                unresolved('HUMAN_NECESSITY_BASIS_MISSING', aid)
            if basis == 'NO_SUITABLE_AUTHORIZED_AI_SURFACE':
                if reevaluation_field != {'state': 'KNOWN', 'value': True}:
                    unresolved('TARGETED_RE_EVALUATION_NOT_ESTABLISHED', aid)
                elif suitable_ai:
                    fail('INVALID_HUMAN_DELEGATION' if definition['deterministic']
                         else 'NO_SUITABLE_AI_SURFACE_CONTRADICTION')
                elif ai_suitability_unknown:
                    unresolved('TARGETED_RE_EVALUATION_NOT_ESTABLISHED',
                               aid + ': AI surface availability is unknown')
        elif actor == 'AI':
            for name, field in (('human_necessity_basis', basis_field),
                                ('targeted_re_evaluation_established', reevaluation_field),
                                ('human_facing_semantics', semantics_field)):
                if field['state'] == 'UNKNOWN':
                    unresolved('REQUIRED_INPUT_UNKNOWN', aid + '.' + name)
                elif field['state'] != 'NOT_REQUIRED':
                    fail('ROUTING_CONTRACT_CONTRADICTION')
        feasible.append({'action_id': aid, 'surface_ids': possible})
        choice = None
        if aid in selected:
            sid = selected[aid]
            if sid not in surfaces:
                fail('SURFACE_CAPABILITY_MISMATCH')
            elif sid not in possible:
                for reason in [r['reason'] for r in rejected if r['action_id'] == aid and r['surface_id'] == sid]:
                    if reason in ('SURFACE_CAPABILITY_MISMATCH', 'SURFACE_RESPONSIBILITY_MISMATCH', 'SURFACE_EFFECT_MISMATCH'):
                        fail(reason)
                        fail('HEADER_BODY_MISMATCH')
                    else:
                        unresolved(reason, aid + ': selected surface ' + sid)
            else:
                choice = sid
        elif possible:
            preferences = [sid for sid in definition['preferred_surfaces'] if sid in possible]
            if preferences:
                choice = preferences[0]
            elif len(possible) == 1:
                choice = possible[0]
            else:
                unresolved('AMBIGUOUS_SURFACE_SELECTION', aid)
        if not possible:
            unresolved('REQUIRED_INPUT_UNKNOWN' if unknown_available else 'REQUIRED_CAPABILITY_UNAVAILABLE', aid)
            unresolved('NO_FEASIBLE_SURFACE_AVAILABLE', aid)
        if actor == 'HUMAN':
            bound_surface_id = choice or selected.get(aid)
            bound_surface = surfaces.get(bound_surface_id, {})
            if human_facing_semantics_issues(semantics_field, {
                    'profile': profile,
                    'action_id': aid,
                    'action_kind': kind,
                    'action_target': required.get('target'),
                    'capabilities': definition['capabilities'],
                    'verification_requirement': required.get('verification_requirement'),
                    'selected_surface_id': bound_surface_id,
                    'selected_surface_label': bound_surface.get('label'),
                    'verification_contract': request.get('verification_contract'),
            }):
                fail('HUMAN_FACING_SEMANTICS_INSUFFICIENT')
        if choice:
            surface = surfaces[choice]
            plan.append({'action_id': aid, 'kind': kind, 'surface_id': choice,
                         'surface_label': surface['label'], 'actor': actor,
                         'capabilities': sorted(definition['capabilities']), 'effects': sorted(effects),
                         'leg_id': 'leg-' + aid, 'session_role': copy.deepcopy(required['session_role']),
                         'execution_surface': {'id': choice, 'label': surface['label']},
                         'assigned_actions': [copy.deepcopy(required)],
                         'required_capabilities': sorted(definition['capabilities']),
                         'effect_conformance': {'required_effects': sorted(effects),
                             'supported_effects': sorted(surface['supported_effects']),
                             'status': 'PASS' if declared_effects is not None else 'UNKNOWN'},
                         'authority_status': assessment['status'], 'model_recommendation': surface['model_recommendation'],
                         'reasoning_recommendation': surface['reasoning_recommendation']})
            for sid in possible:
                if sid != choice:
                    rejected.append({'action_id': aid, 'surface_id': sid, 'reason': 'FEASIBLE_NOT_SELECTED'})

    if not failures and not issues and len(plan) != len(ids):
        fail('ROUTING_CONTRACT_CONTRADICTION')
    status = 'FAIL' if failures else ('UNRESOLVED' if issues else 'PASS')
    chosen_ids = sorted({step['surface_id'] for step in plan})
    mode = ('COMPOSITE' if len(chosen_ids) > 1 else 'SINGLE') if len(plan) == len(ids) else 'UNSELECTED'
    result = {
        'schema_version': '1.3', 'routing_result_id': 'pending', 'request_id': request['request_id'],
        'routing_status': status, 'project': copy.deepcopy(request['project']),
        'destination_session_role': copy.deepcopy(request['destination_session_role']), 'route_mode': mode,
        'required_capabilities': sorted(capabilities), 'feasible_surfaces': feasible,
        'execution_plan': plan, 'rejected_alternatives': rejected,
        'responsibility_allocation': dict(copy.deepcopy(request['responsibility']), execution=[
            {k: step[k] for k in ('action_id', 'actor', 'surface_id')} for step in plan]),
        'authority_assessment': assessments,
        'model_recommendation': [{'surface_id': sid, 'value': surfaces[sid]['model_recommendation']} for sid in chosen_ids],
        'reasoning_recommendation': [{'surface_id': sid, 'value': surfaces[sid]['reasoning_recommendation']} for sid in chosen_ids],
        'routing_profile': {'id': profile['id'], 'version': profile['version']}, 'validator_version': VERSION,
        'failure_codes': sorted(failures), 'unresolved_issues': sorted(issues, key=lambda x: (x['code'], x['detail'])),
        'resolution_action': resolution_actions(failures + [i['code'] for i in issues]),
        'semantic_fingerprint': 'pending', 'source_request': copy.deepcopy(request), 'source_profile': copy.deepcopy(profile)
    }
    for key in ('approved_execution_boundary', 'prohibited_actions', 'verification_contract', 'return_contract'):
        result[key] = copy.deepcopy(request[key])
    result['semantic_fingerprint'] = fingerprint(result)
    result['routing_result_id'] = 'routing-' + result['semantic_fingerprint']
    validate_internal_conformance(result)
    deadline.check()
    return result


def diagnostic(code, detail, status='UNRESOLVED'):
    return {'routing_status': status, 'failure_codes': [code] if status == 'FAIL' else [],
            'unresolved_issues': [] if status == 'FAIL' else [{'code': code, 'detail': detail}],
            'resolution_action': resolution_actions([code]),
            'result': None, 'directive': None}


def evaluate(request, profile, timeout_seconds=5.0):
    """All public routing failures return a non-executable diagnostic envelope."""
    try:
        result = _evaluate(copy.deepcopy(request), copy.deepcopy(profile), Deadline(timeout_seconds))
        return {'routing_status': result['routing_status'], 'failure_codes': result['failure_codes'],
                'unresolved_issues': result['unresolved_issues'], 'resolution_action': result['resolution_action'],
                'result': result, 'directive': None}
    except InvalidDocument as error:
        return diagnostic('ROUTING_CONTRACT_CONTRADICTION', str(error), 'FAIL')
    except TimeoutError as error:
        return diagnostic('VALIDATOR_TIMEOUT', str(error))
    except Exception as error:
        return diagnostic('VALIDATOR_ERROR', type(error).__name__)


def verify_result(result, timeout_seconds=5.0):
    """Recompute the complete contract; a hash alone never establishes validity."""
    try:
        validate(result, 'routing-result')
        envelope = evaluate(result['source_request'], result['source_profile'], timeout_seconds)
        if envelope['result'] is None:
            return envelope
        if result != envelope['result']:
            return diagnostic('MATERIAL_DIRECTIVE_DRIFT', 'structured contract changed; revalidate', 'FAIL')
        return envelope
    except InvalidDocument as error:
        return diagnostic('ROUTING_CONTRACT_CONTRADICTION', str(error), 'FAIL')
    except Exception as error:
        return diagnostic('VALIDATOR_ERROR', type(error).__name__)
