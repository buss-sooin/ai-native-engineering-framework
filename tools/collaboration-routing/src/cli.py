"""JSON stdout only; exit codes: PASS=0, FAIL=1, UNRESOLVED=2."""
import argparse
import json
import sys
from pathlib import Path

from directive import render, validate_directive
from engine import diagnostic, evaluate, validate_profile
from schema_validation import InvalidDocument, load_json, validate


def main(argv=None):
    parser = argparse.ArgumentParser(description='Local routing contract validation; never executes routed actions.')
    commands = parser.add_subparsers(dest='command', required=True)
    for command in ('route', 'validate-directive'):
        child = commands.add_parser(command)
        child.add_argument('--request', required=True)
        child.add_argument('--profile', required=True)
        child.add_argument('--timeout-seconds', type=float, default=5.0)
        if command == 'validate-directive':
            child.add_argument('--result', required=True, help='Raw result JSON, not the CLI envelope')
            child.add_argument('--directive', required=True)
    child = commands.add_parser('validate-schema')
    child.add_argument('--kind', choices=['routing-request', 'routing-result', 'project-routing-profile'], required=True)
    child.add_argument('--document', required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == 'validate-schema':
            document = load_json(args.document)
            if args.kind == 'project-routing-profile':
                validate_profile(document)
            else:
                validate(document, args.kind)
            envelope = {'routing_status': 'PASS', 'validation_scope': 'SCHEMA_ONLY', 'directive': None}
        else:
            envelope = evaluate(load_json(args.request), load_json(args.profile), args.timeout_seconds)
            if envelope['routing_status'] == 'PASS':
                if args.command == 'route':
                    envelope = render(envelope['result'], args.timeout_seconds)
                else:
                    supplied = load_json(args.result)
                    # Verify against caller-supplied source files, not only embedded snapshots.
                    if supplied != envelope['result']:
                        envelope = diagnostic('MATERIAL_DIRECTIVE_DRIFT', 'result differs from current request/profile', 'FAIL')
                    else:
                        envelope = validate_directive(supplied, Path(args.directive).read_text(encoding='utf-8'), args.timeout_seconds)
    except (InvalidDocument, json.JSONDecodeError) as error:
        envelope = diagnostic('ROUTING_CONTRACT_CONTRADICTION', str(error), 'FAIL')
    except Exception as error:
        envelope = diagnostic('VALIDATOR_ERROR', type(error).__name__)
    print(json.dumps(envelope, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False))
    return {'PASS': 0, 'FAIL': 1, 'UNRESOLVED': 2}[envelope['routing_status']]


if __name__ == '__main__':
    sys.exit(main())
