import collections
import itertools
import re
import typing

from horkos import cataloger
from horkos import schemaomatic


class Critique(typing.NamedTuple):
    """A critique of a dataschema."""

    scope: str
    code: str
    message: str

############################
#
# WITHIN DATASET
#
############################
#
# Fields
# - Naming
# -

# Data sets


# Field naming
# Data set naming
# Names should mean the same thing
# Type consistency
# Documentation length

CAMEL_REGEX = re.compile(r'^[a-z]+([A-Z][a-z]*)*$')
CAPS_REGEX = re.compile(r'^([A-Z]+_{0,1})*[A-Z]+$')
PASCAL_REGEX = re.compile(r'^([A-Z][a-z]*)+$')
SNAKE_REGEX = re.compile(r'^([a-z]+_{0,1})*[a-z]+$')
CASE_MAP = {
    'CAPS_CASE': CAPS_REGEX,
    'camelCase': CAMEL_REGEX,
    'PascalCase': PASCAL_REGEX,
    'snake_case': SNAKE_REGEX,
}


def _casing_type(value: str) -> list:
    """Determine which casing types the value adheres to."""
    return [case for case, regex in CASE_MAP.items() if regex.match(value)]


def _most_common_casing_type(values: typing.List[str]) -> typing.Tuple:
    """Identify the most common casing type from the list of strings."""
    counter = collections.Counter(
        itertools.chain.from_iterable(
          _casing_type(value) for value in values
        )
    )
    common = counter.most_common()
    if not common:
        return [], 0
    count = common[0][1]
    casings = [c for c in CASE_MAP if counter[c] == count]
    return casings, count


def _oxford_join(values: typing.List[str], last: str = 'and') -> str:
    """Join the given strings into an english list."""
    if not values:
        return ''
    if len(values) == 1:
        return values[0]
    working = values.copy()
    working[-1] = f'{last} {working[-1]}'
    joiner = ', ' if len(values) > 2 else ' '
    return joiner.join(working)


def schema_uniform_field_casing_check(
        schema: schemaomatic.Schema
) -> typing.Optional[Critique]:
    """Within a schema fields should have uniform casing."""
    casings, count = _most_common_casing_type(schema.fields.keys())
    if count != len(schema.fields):
        verb = 'is' if len(casings) == 1 else 'are'
        suggestions = _oxford_join(casings)
        closest = (
            ''
            if count == 0
            else f' {suggestions} {verb} most common with {count} matching.'
        )
        options = ', '.join(CASE_MAP)
        msg = (
            'No clear casing convention, consider using any of the following: '
            f'{options}.{closest}'
        )
        return Critique('schema', 'internally_field_consistency', msg)
    return None


def relative_field_casing_check(
        schema: schemaomatic.Schema, catalog: cataloger.Catalog
) -> typing.Optional[Critique]:
    """
    When comparing a schema against a catalog the schema should have
    casing conventions that are consistent with the catalog.
    """
    if schema.name in catalog.schemas:
        raise ValueError(f'schema named {schema.name} already in catalog.')
    fields = list(itertools.chain.from_iterable(
        schema.fields.keys() for schema in catalog.schemas.values()
    ))
    catalog_casings, catalog_count = _most_common_casing_type(fields)
    non_existing = set(schema.fields.keys()) - set(fields)
    casing, _ = _most_common_casing_type(non_existing)
    either_empty = not catalog_casings or not non_existing
    if set(casing).intersection(catalog_casings) or either_empty:
        return None
    percentage = int(catalog_count * 100 / (len(fields) or 1))
    conventions = _oxford_join(catalog_casings, last = 'or')
    schema_convs = _oxford_join(casing)
    verb = 's are' if len(casing) != 1 else ' is'
    schema_msg = (
        f' Among new fields the dominant convention{verb} {schema_convs}'
        if casing else
        ''
    )
    msg = (
        'The casing convention of new fields do not match the dominant '
        f'patterns of the catalog. {percentage}% of fields in the catalog '
        f'follow {conventions}.{schema_msg}'
    )
    return Critique('relative', 'relative_field_consistency', msg)
