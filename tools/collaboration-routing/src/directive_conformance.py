"""Independent semantic validation for rendered routing directives.

This module intentionally does not import or invoke the Renderer. It parses the
human-visible projection and compares every decision-bearing value with the
validated Routing Result.
"""
import html
import json

from engine import verify_result
from semantic_sufficiency import (
    human_execution_projection_issues,
    resolve_human_execution_responsibility,
)


HEADER_FIELDS = (
    'ChatGPT Project / Workspace',
    'Recommended Session / Work Title',
    'Destination Session Role',
    'Execution Surface',
    'Recommended Model',
    'Recommended Reasoning Level',
)


def _failure(code, detail):
    return {'status': 'FAIL', 'failure_codes': [code], 'detail': detail}


def _heading(value):
    text = html.escape(value, quote=False).replace('\\', '\\\\')
    for char in '`*_[]#':
        text = text.replace(char, '\\' + char)
    return text.replace('\r', '&#13;').replace('\n', '&#10;')


def _normalized_lines(text):
    if not isinstance(text, str):
        raise TypeError('directive must be text')
    return [line.rstrip(' \t') for line in text.replace('\r\n', '\n').split('\n') if line.strip(' \t')]


def _parse_json(value):
    return json.loads(value)


def _expected_headers(result):
    plan = result['execution_plan']
    surfaces = sorted({(step['actor'], step['surface_id'], step['surface_label']) for step in plan})
    return {
        'ChatGPT Project / Workspace': result['project']['value'],
        'Recommended Session / Work Title': result['source_request']['title']['value'],
        'Destination Session Role': result['destination_session_role']['value'],
        'Execution Surface': [
            {'responsibility': actor, 'surface': label} for actor, _, label in surfaces
        ],
        'Recommended Model': result['model_recommendation'],
        'Recommended Reasoning Level': result['reasoning_recommendation'],
    }


def _human_execution_responsibilities(plan, profile):
    responsibilities = []
    for step in plan:
        if step['actor'] != 'HUMAN':
            continue
        action = step['assigned_actions'][0]
        responsibilities.append(resolve_human_execution_responsibility(
            action, step, profile))
    return responsibilities


def _expected_sections(result):
    request = result['source_request']
    plan = result['execution_plan']
    sections = [
        ('Engineering Objective', request['objective']['value'], 'OBJECTIVE_MISMATCH'),
        ('Applicable Canonical Authority / Target', {
            'canonical_authority': request['canonical_authority'], 'target': request['target']
        }, 'CANONICAL_CONTEXT_MISMATCH'),
        ('Current State / Current Gate', {
            'current_state': request['current_state'], 'current_gate': request['current_gate']
        }, 'CURRENT_STATE_MISMATCH'),
        ('Approved Execution Boundary / Authority Status', {
            'boundary': result['approved_execution_boundary'], 'authority': result['authority_assessment']
        }, 'AUTHORITY_MISMATCH'),
        ('Required Responsibility', {
            'allocation': result['responsibility_allocation'],
            'required_actions': request['required_actions'],
            'AI Session Surface': [step for step in plan if step['actor'] == 'AI'],
            'Human Execution Surface': [step for step in plan if step['actor'] == 'HUMAN'],
        }, 'RESPONSIBILITY_MISMATCH'),
    ]
    human_responsibilities = _human_execution_responsibilities(plan, result['source_profile'])
    if human_responsibilities:
        sections.append(('Human Execution Responsibility', human_responsibilities,
                         'HUMAN_EXECUTION_SEMANTICS_MISMATCH'))
    sections.extend([
        ('Prohibited / Out-of-scope Action', result['prohibited_actions'], 'PROHIBITED_ACTION_MISMATCH'),
        ('Verification / Expected Result', result['verification_contract'], 'VERIFICATION_MISMATCH'),
        ('Return / Closure Destination', result['return_contract'], 'RETURN_DESTINATION_MISMATCH'),
    ])
    for title, field in (
        ('Stop Conditions', 'stop_conditions'),
        ('Evidence Requirement', 'evidence_requirement'),
        ('Branch / Revision / Environment', 'branch_revision_environment'),
    ):
        if request[field]['state'] != 'NOT_REQUIRED':
            sections.append((title, request[field], 'REQUIRED_HANDOFF_CONTEXT_MISMATCH'))
    approvals = [item for item in result['authority_assessment']
                 if item['approval_reference']['state'] == 'KNOWN']
    if approvals:
        sections.append(('Approval Reference', approvals, 'AUTHORITY_MISMATCH'))
    sections.append(('Routing Verification', {
        'routing_result_id': result['routing_result_id'],
        'semantic_fingerprint': result['semantic_fingerprint'],
        'routing_profile': result['routing_profile'],
        'validator_version': result['validator_version'],
    }, 'RESULT_DIRECTIVE_INTEGRITY_MISMATCH'))
    return sections


def validate_directive_conformance(result, text, timeout_seconds=5.0):
    """Validate directive topology and semantics without calling the Renderer."""
    verified = verify_result(result, timeout_seconds)
    if verified['routing_status'] != 'PASS':
        return _failure('ROUTING_RESULT_INVALID', 'Routing Result is not a validated PASS result.')
    try:
        lines = _normalized_lines(text)
        if not lines or lines[0] != '## Routing Header':
            code = 'ROUTING_HEADER_NOT_FIRST' if '## Routing Header' in lines else 'ROUTING_HEADER_MISSING'
            return _failure(code, 'Routing Header must be the first directive content.')

        expected_headers = _expected_headers(result)
        actual_headers = {}
        position = 1
        mismatch_codes = {
            'ChatGPT Project / Workspace': 'PROJECT_WORKSPACE_MISMATCH',
            'Recommended Session / Work Title': 'SESSION_TITLE_MISMATCH',
            'Destination Session Role': 'DESTINATION_SESSION_ROLE_MISMATCH',
            'Execution Surface': 'EXECUTION_SURFACE_MISMATCH',
            'Recommended Model': 'MODEL_RECOMMENDATION_MISMATCH',
            'Recommended Reasoning Level': 'REASONING_RECOMMENDATION_MISMATCH',
        }
        for field in HEADER_FIELDS:
            prefix = '- ' + field + ': '
            if position >= len(lines) or not lines[position].startswith(prefix):
                return _failure('ROUTING_HEADER_FIELD_MISSING', 'Missing or reordered Routing Header field: ' + field)
            actual = _parse_json(lines[position][len(prefix):])
            actual_headers[field] = actual
            if actual != expected_headers[field]:
                code = mismatch_codes[field]
                if field == 'Destination Session Role':
                    surface_labels = {item['surface'] for item in expected_headers['Execution Surface']}
                    if actual in surface_labels or isinstance(actual, (dict, list)):
                        code = 'ROLE_SURFACE_CONFLATION'
                return _failure(code, field + ' differs from the Routing Result.')
            position += 1

        if actual_headers['Destination Session Role'] == actual_headers['Execution Surface']:
            return _failure('ROLE_SURFACE_CONFLATION', 'Session Role and Execution Surface are distinct fields.')

        expected_title = '# ' + _heading(result['source_request']['title']['value'])
        if position >= len(lines) or lines[position] != expected_title:
            return _failure('SESSION_TITLE_MISMATCH', 'Directive title differs from the Routing Result context.')
        position += 1

        for title, expected_value, mismatch_code in _expected_sections(result):
            if position >= len(lines) or lines[position] != '## ' + title:
                return _failure('REQUIRED_HANDOFF_CONTEXT_MISSING', 'Missing or reordered section: ' + title)
            if position + 3 >= len(lines) or lines[position + 1] != '```json' or lines[position + 3] != '```':
                return _failure('DIRECTIVE_STRUCTURE_INVALID', 'Invalid JSON block for section: ' + title)
            actual_value = _parse_json(lines[position + 2])
            if title == 'Human Execution Responsibility':
                issues = human_execution_projection_issues(
                    actual_value, result['execution_plan'], result['source_profile'])
                if issues:
                    return _failure('HUMAN_FACING_SEMANTICS_INSUFFICIENT',
                                    'Insufficient Human-facing fields: ' + ', '.join(issues))
            if actual_value != expected_value:
                return _failure(mismatch_code, title + ' differs from the Routing Result or immutable request context.')
            position += 4

        if position != len(lines):
            return _failure('UNEXPECTED_DIRECTIVE_CONTENT', 'Directive contains content outside the validated contract.')
        return {'status': 'PASS', 'failure_codes': [], 'detail': 'Directive conforms to the validated Routing Result.'}
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
        return _failure('DIRECTIVE_STRUCTURE_INVALID', type(error).__name__)
