"""Strict validator for the JSON Schema subset used by the bundled contracts.

Not a general-purpose JSON Schema implementation. Unsupported keywords fail closed.
"""
import json
from pathlib import Path

SCHEMAS = Path(__file__).resolve().parents[1] / 'schemas'
KEYWORDS = {'$schema', '$id', 'type', 'properties', 'required', 'additionalProperties',
            'items', 'minItems', 'uniqueItems', 'minLength', 'enum', 'oneOf'}


class SchemaError(ValueError):
    pass


class InvalidDocument(ValueError):
    pass


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)


def load_json(path):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise InvalidDocument('duplicate JSON key: ' + key)
            result[key] = value
        return result

    def constant(value):
        raise InvalidDocument('non-finite JSON number: ' + value)

    return json.loads(Path(path).read_text(encoding='utf-8'), object_pairs_hook=pairs,
                      parse_constant=constant)


def check_schema(schema):
    if not isinstance(schema, dict) or set(schema) - KEYWORDS:
        raise SchemaError('unsupported schema structure or keyword')
    if 'type' in schema and schema['type'] not in ('object', 'array', 'string', 'boolean'):
        raise SchemaError('unsupported schema type')
    for child in schema.get('properties', {}).values():
        check_schema(child)
    if 'items' in schema:
        check_schema(schema['items'])
    for child in schema.get('oneOf', []):
        check_schema(child)


def _validate(value, schema, path):
    if 'oneOf' in schema:
        count = 0
        for option in schema['oneOf']:
            try:
                _validate(value, option, path)
                count += 1
            except InvalidDocument:
                pass
        if count != 1:
            raise InvalidDocument(path + ': expected exactly one state/shape')
    if 'enum' in schema and not any(type(value) is type(v) and value == v for v in schema['enum']):
        raise InvalidDocument(path + ': invalid enum value')
    kind = schema.get('type')
    types = {'object': dict, 'array': list, 'string': str, 'boolean': bool}
    if kind and type(value) is not types[kind]:
        raise InvalidDocument(path + ': expected ' + kind)
    if kind == 'object':
        if set(schema['required']) - set(value):
            raise InvalidDocument(path + ': missing required fields')
        if schema.get('additionalProperties') is False and set(value) - set(schema['properties']):
            raise InvalidDocument(path + ': unexpected fields')
        for key, item in value.items():
            _validate(item, schema['properties'][key], path + '.' + key)
    elif kind == 'array':
        if len(value) < schema.get('minItems', 0):
            raise InvalidDocument(path + ': too few items')
        if schema.get('uniqueItems') and len(set(map(canonical, value))) != len(value):
            raise InvalidDocument(path + ': duplicate items')
        for index, item in enumerate(value):
            _validate(item, schema['items'], path + '[' + str(index) + ']')
    elif kind == 'string':
        if len(value.strip()) < schema.get('minLength', 0):
            raise InvalidDocument(path + ': empty text')


def validate(value, name):
    schema = load_json(SCHEMAS / (name + '.schema.json'))
    check_schema(schema)
    _validate(value, schema, '$')
