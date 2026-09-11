"""Deterministic Markdown projection with conservative semantic conformance."""
import html
from engine import diagnostic, resolution_actions, verify_result
from schema_validation import canonical
from semantic_sufficiency import resolve_human_execution_responsibility


def literal(value):
    # Keep untrusted text on one line and prevent Markdown/HTML fence injection.
    return canonical(value).replace('`', '\\u0060').replace('<', '\\u003c').replace('>', '\\u003e')


def heading(value):
    text = html.escape(value, quote=False).replace('\\', '\\\\')
    for char in '`*_[]#':
        text = text.replace(char, '\\' + char)
    return text.replace('\r', '&#13;').replace('\n', '&#10;')


def human_execution_responsibilities(plan, profile):
    responsibilities = []
    for step in plan:
        if step['actor'] != 'HUMAN':
            continue
        action = step['assigned_actions'][0]
        responsibilities.append(resolve_human_execution_responsibility(
            action, step, profile))
    return responsibilities


def _render(result):
    request = result['source_request']
    plan = result['execution_plan']
    surfaces = sorted({(s['actor'], s['surface_id'], s['surface_label']) for s in plan})
    surface_text = [{'responsibility': actor, 'surface': label} for actor, _, label in surfaces]
    headers = [('ChatGPT Project / Workspace', request['project']['value']),
               ('Recommended Session / Work Title', request['title']['value']),
               ('Destination Session Role', request['destination_session_role']['value']),
               ('Execution Surface', surface_text),
               ('Recommended Model', result['model_recommendation']),
               ('Recommended Reasoning Level', result['reasoning_recommendation'])]
    lines = ['## Routing Header', ''] + ['- ' + k + ': ' + literal(v) for k, v in headers]
    lines.extend(['', '# ' + heading(request['title']['value'])])
    sections = [
        ('Engineering Objective', request['objective']['value']),
        ('Applicable Canonical Authority / Target', {'canonical_authority': request['canonical_authority'], 'target': request['target']}),
        ('Current State / Current Gate', {'current_state': request['current_state'], 'current_gate': request['current_gate']}),
        ('Approved Execution Boundary / Authority Status', {'boundary': result['approved_execution_boundary'], 'authority': result['authority_assessment']}),
        ('Required Responsibility', {'allocation': result['responsibility_allocation'], 'required_actions': request['required_actions'],
                                     'AI Session Surface': [s for s in plan if s['actor'] == 'AI'],
                                     'Human Execution Surface': [s for s in plan if s['actor'] == 'HUMAN']}),
    ]
    human_responsibilities = human_execution_responsibilities(plan, result['source_profile'])
    if human_responsibilities:
        sections.append(('Human Execution Responsibility', human_responsibilities))
    sections.extend([
        ('Prohibited / Out-of-scope Action', result['prohibited_actions']),
        ('Verification / Expected Result', result['verification_contract']),
        ('Return / Closure Destination', result['return_contract'])])
    for title, field in [('Stop Conditions', 'stop_conditions'), ('Evidence Requirement', 'evidence_requirement'),
                         ('Branch / Revision / Environment', 'branch_revision_environment')]:
        if request[field]['state'] != 'NOT_REQUIRED':
            sections.append((title, request[field]))
    approvals = [a for a in result['authority_assessment'] if a['approval_reference']['state'] == 'KNOWN']
    if approvals:
        sections.append(('Approval Reference', approvals))
    sections.append(('Routing Verification', {'routing_result_id': result['routing_result_id'],
                     'semantic_fingerprint': result['semantic_fingerprint'], 'routing_profile': result['routing_profile'],
                     'validator_version': result['validator_version']}))
    for title, value in sections:
        lines.extend(['', '## ' + title, '', '```json', literal(value), '```'])
    return '\n'.join(lines) + '\n'


def normalize_markdown(text):
    # Cosmetic allowances are intentionally narrow: CRLF, empty lines, trailing spaces.
    # Never collapse spaces within task text, JSON strings, or code.
    return '\n'.join(line.rstrip(' \t') for line in text.replace('\r\n', '\n').split('\n') if line.strip(' \t'))


def validate_directive(result, text, timeout_seconds=5.0):
    envelope = verify_result(result, timeout_seconds)
    if envelope['routing_status'] != 'PASS':
        return envelope
    try:
        expected = _render(result)
        if normalize_markdown(text) != normalize_markdown(expected):
            error = diagnostic('MATERIAL_DIRECTIVE_DRIFT', 'directive changed; revalidate', 'FAIL')
            if normalize_markdown(text.split('## Engineering Objective')[0]) != normalize_markdown(expected.split('## Engineering Objective')[0]):
                error['failure_codes'].append('HEADER_BODY_MISMATCH')
                error['resolution_action'] = resolution_actions(error['failure_codes'])
            return error
        envelope['directive'] = text
        return envelope
    except Exception as error:
        return diagnostic('VALIDATOR_ERROR', type(error).__name__)


def render(result, timeout_seconds=5.0):
    envelope = verify_result(result, timeout_seconds)
    if envelope['routing_status'] != 'PASS':
        return envelope
    try:
        return validate_directive(result, _render(result), timeout_seconds)
    except Exception as error:
        return diagnostic('VALIDATOR_ERROR', type(error).__name__)
