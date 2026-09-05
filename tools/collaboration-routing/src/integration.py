"""Operator-mediated integration adapter for deterministic routing emission."""
import copy
import hashlib

from directive import render
from directive_conformance import validate_directive_conformance
from engine import evaluate, validate_profile
from schema_validation import canonical, validate


VERSION = '0.1.0'
_DEFAULT = object()


def _fingerprint(value):
    try:
        return hashlib.sha256(canonical(value).encode('utf-8')).hexdigest()
    except Exception:
        return None


def _evidence(request, result, rendered_directive, validation_result, outcome):
    return {
        'integration_version': VERSION,
        'request_id': request.get('request_id') if isinstance(request, dict) else None,
        'routing_result_id': result.get('routing_result_id') if isinstance(result, dict) else None,
        'routing_request_fingerprint': _fingerprint(request),
        'routing_result_fingerprint': _fingerprint(result),
        'routing_semantic_fingerprint': result.get('semantic_fingerprint') if isinstance(result, dict) else None,
        'rendered_directive_fingerprint': _fingerprint(rendered_directive),
        'directive_validation_fingerprint': _fingerprint(validation_result),
        'emission_outcome': outcome,
    }


def integration_blocked(code, stage, detail, request=None, result=None,
                        rendered_directive=None, validation_result=None):
    if validation_result is None:
        validation_result = {
            'status': 'NOT_RUN', 'failure_codes': [], 'detail': 'Directive validation did not complete.'
        }
    return {
        'integration_status': 'INTEGRATION_BLOCKED',
        'routing_status': result.get('routing_status') if isinstance(result, dict) else None,
        'failure_codes': [],
        'unresolved_issues': [],
        'resolution_action': [{
            'kind': 'INTEGRATION_RESOLUTION', 'causes': [code],
            'instruction': 'Resolve the integration failure and rerun the complete flow; do not emit or reuse a directive.'
        }],
        'integration_diagnostics': [{'code': code, 'stage': stage, 'detail': detail}],
        'result': result,
        'directive_validation': validation_result,
        'directive': None,
        'emission_outcome': 'BLOCKED',
        'evidence': _evidence(request, result, rendered_directive, validation_result, 'BLOCKED'),
    }


def _routing_blocked(request, envelope):
    result = envelope['result']
    validation_result = {
        'status': 'NOT_RUN', 'failure_codes': [],
        'detail': 'Semantic Routing Result is not PASS; directive rendering is prohibited.'
    }
    return {
        'integration_status': 'BLOCKED_BY_ROUTING',
        'routing_status': envelope['routing_status'],
        'failure_codes': envelope['failure_codes'],
        'unresolved_issues': envelope['unresolved_issues'],
        'resolution_action': envelope['resolution_action'],
        'integration_diagnostics': [],
        'result': result,
        'directive_validation': validation_result,
        'directive': None,
        'emission_outcome': 'BLOCKED',
        'evidence': _evidence(request, result, None, validation_result, 'BLOCKED'),
    }


def integrate(request, profile, timeout_seconds=5.0, engine_callable=_DEFAULT,
              renderer_callable=_DEFAULT, validator_callable=_DEFAULT):
    """Return a directive only after a validated PASS result and independent validation."""
    request_snapshot, profile_snapshot = copy.deepcopy(request), copy.deepcopy(profile)
    try:
        validate(request_snapshot, 'routing-request')
    except Exception as error:
        return integration_blocked('ROUTING_REQUEST_INVALID', 'REQUEST_VALIDATION',
                                   type(error).__name__, request_snapshot)
    try:
        validate_profile(profile_snapshot)
    except Exception as error:
        return integration_blocked('ROUTING_PROFILE_INVALID', 'REQUEST_VALIDATION',
                                   type(error).__name__, request_snapshot)

    if engine_callable is _DEFAULT:
        engine_callable = evaluate
    if renderer_callable is _DEFAULT:
        renderer_callable = render
    if validator_callable is _DEFAULT:
        validator_callable = validate_directive_conformance
    if engine_callable is None:
        return integration_blocked('ENGINE_UNAVAILABLE', 'ENGINE_INVOCATION',
                                   'Routing Engine is unavailable.', request_snapshot)
    try:
        envelope = engine_callable(request_snapshot, profile_snapshot, timeout_seconds)
    except Exception as error:
        return integration_blocked('ENGINE_INVOCATION_ERROR', 'ENGINE_INVOCATION',
                                   type(error).__name__, request_snapshot)

    required_envelope_fields = ('routing_status', 'failure_codes', 'unresolved_issues',
                                'resolution_action', 'result', 'directive')
    if (not isinstance(envelope, dict)
            or any(field not in envelope for field in required_envelope_fields)
            or envelope.get('routing_status') not in ('PASS', 'FAIL', 'UNRESOLVED')):
        return integration_blocked('ENGINE_RESULT_INVALID', 'ENGINE_RESULT_VALIDATION',
                                   'Routing Engine returned an invalid envelope.', request_snapshot)
    result = envelope.get('result')
    if result is None:
        return integration_blocked('ENGINE_RESULT_UNAVAILABLE', 'ENGINE_RESULT_VALIDATION',
                                   'Routing Engine did not return a semantic Routing Result.', request_snapshot)
    if not isinstance(result, dict):
        return integration_blocked('ENGINE_RESULT_INVALID', 'ENGINE_RESULT_VALIDATION',
                                   'Routing Engine result has an invalid shape.', request_snapshot)
    if result.get('routing_status') != envelope['routing_status']:
        return integration_blocked('ENGINE_RESULT_MISMATCH', 'ENGINE_RESULT_VALIDATION',
                                   'Envelope status differs from the Routing Result.', request_snapshot, result)
    if envelope['routing_status'] != 'PASS':
        return _routing_blocked(request_snapshot, envelope)

    if renderer_callable is None:
        return integration_blocked('RENDERER_UNAVAILABLE', 'RENDERING',
                                   'Renderer is unavailable.', request_snapshot, result)
    try:
        rendered = renderer_callable(result, timeout_seconds)
    except Exception as error:
        return integration_blocked('RENDERER_ERROR', 'RENDERING', type(error).__name__, request_snapshot, result)
    if not isinstance(rendered, dict) or rendered.get('routing_status') != 'PASS' or not isinstance(rendered.get('directive'), str):
        return integration_blocked('RENDERER_REJECTED', 'RENDERING',
                                   'Renderer did not produce a PASS directive.', request_snapshot, result)
    rendered_directive = rendered['directive']

    if validator_callable is None:
        return integration_blocked('DIRECTIVE_VALIDATOR_UNAVAILABLE', 'DIRECTIVE_VALIDATION',
                                   'Directive Validator is unavailable.', request_snapshot, result, rendered_directive)
    try:
        validation_result = validator_callable(result, rendered_directive, timeout_seconds)
    except Exception as error:
        return integration_blocked('DIRECTIVE_VALIDATOR_ERROR', 'DIRECTIVE_VALIDATION',
                                   type(error).__name__, request_snapshot, result, rendered_directive)
    if not isinstance(validation_result, dict) or validation_result.get('status') != 'PASS':
        return integration_blocked('DIRECTIVE_CONFORMANCE_REJECTED', 'DIRECTIVE_VALIDATION',
                                   'Independent Directive Validator rejected the rendered directive.',
                                   request_snapshot, result, rendered_directive, validation_result)

    return {
        'integration_status': 'PASS',
        'routing_status': 'PASS',
        'failure_codes': [],
        'unresolved_issues': [],
        'resolution_action': [],
        'integration_diagnostics': [],
        'result': result,
        'directive_validation': validation_result,
        'directive': rendered_directive,
        'emission_outcome': 'EMITTED',
        'evidence': _evidence(request_snapshot, result, rendered_directive, validation_result, 'EMITTED'),
    }
