"""JSON CLI for the operator-mediated routing integration trial."""
import argparse
import json
import sys

from integration import integrate, integration_blocked
from schema_validation import load_json


def main(argv=None):
    parser = argparse.ArgumentParser(
        description='Operator-mediated routing integration; never executes routed actions.')
    parser.add_argument('--request', required=True)
    parser.add_argument('--profile', required=True)
    parser.add_argument('--timeout-seconds', type=float, default=5.0)
    args = parser.parse_args(argv)
    try:
        request = load_json(args.request)
        profile = load_json(args.profile)
        envelope = integrate(request, profile, args.timeout_seconds)
    except Exception as error:
        envelope = integration_blocked('REQUEST_SERIALIZATION_INVALID', 'REQUEST_DESERIALIZATION',
                                       type(error).__name__)
    print(json.dumps(envelope, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False))
    if envelope['integration_status'] == 'PASS':
        return 0
    if envelope['integration_status'] == 'INTEGRATION_BLOCKED':
        return 3
    return 1 if envelope['routing_status'] == 'FAIL' else 2


if __name__ == '__main__':
    sys.exit(main())
