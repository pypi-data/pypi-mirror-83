import collections
import itertools
import re
import typing


from horkos import cataloger
from horkos.critiquer import _utils
from horkos.critiquer import _definitions
from horkos import schemaomatic


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


def local_uniform_field_casing_check(
        schema: schemaomatic.Schema
) -> typing.Optional[_definitions.Critique]:
    """Within a schema fields should have uniform casing."""
    casings, count = _most_common_casing_type(schema.fields.keys())
    if count != len(schema.fields):
        verb = 'is' if len(casings) == 1 else 'are'
        suggestions = _utils.oxford_join(casings)
        closest = (
            ''
            if count == 0
            else f' {suggestions} {verb} most common with {count} matching.'
        )
        msg = (
            f'No clear casing convention.{closest}'
        )
        return _definitions.Critique('local', 'field_consistency', msg)
    return None


def relative_field_casing_check(
        schema: schemaomatic.Schema, catalog: cataloger.Catalog
) -> typing.Optional[_definitions.Critique]:
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
    conventions = _utils.oxford_join(catalog_casings, last = 'or')
    schema_convs = _utils.oxford_join(casing)
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
    return _definitions.Critique('relative', 'field_consistency', msg)


def global_field_casing_check(
        catalog: cataloger.Catalog
) -> typing.Optional[_definitions.Critique]:
    """
    Naming conventions should be consistent across all fields in a catalog.

    :param catalog:
        The group of schemas to check for uniformity.
    :return:
        A _definitions.Critique if one is found, otherwise nothing.
    """
    fields = list(itertools.chain.from_iterable(
        schema.fields.keys() for schema in catalog.schemas.values()
    ))
    casings, count = _most_common_casing_type(fields)
    if len(fields) == count:
        return None
    verb = 'is' if len(casings) == 1 else 'are'
    suggestions = _utils.oxford_join(casings)
    percentage = int(count * 100 / (len(fields) or 1))
    closest = (
        ''
        if count == 0
        else f' {suggestions} {verb} most common with {percentage}% matching.'
    )
    msg = f'No clear casing convention.{closest}'
    return _definitions.Critique('global', 'field_consistency', msg)


def local_prefer_snake_case(
        schema: schemaomatic.Schema
) -> typing.Optional[_definitions.Critique]:
    """
    snake_case should be the preferred.

    :param schema:
        The schema to validate for snake_case usage.
    :return:
        A _definitions.Critique if one is found, otherwise nothing.
    """
    casings, _ = _most_common_casing_type(schema.fields)
    if 'snake_case' in casings:
        return None
    joined = _utils.oxford_join(casings, last="or")
    current = (
        ''
        if not casings else
        f' Schema is currently using {joined}.'
    )
    msg = (
        'snake_case field names are recommended for the greatest '
        f'compatibility with common big data technologies.{current}'
    )
    return _definitions.Critique('local', 'recommend_snake_case', msg)


def global_prefer_snake_case(
        catalog: cataloger.Catalog
) -> typing.Optional[_definitions.Critique]:
    """
    snake_case should be the preferred.

    :param catalog:
        The catalog to validate for snake_case usage.
    :return:
        A _definitions.Critique if one is found, otherwise nothing.
    """
    fields = list(itertools.chain.from_iterable(
        schema.fields.keys() for schema in catalog.schemas.values()
    ))

    casings, _ = _most_common_casing_type(fields)
    if 'snake_case' in casings:
        return None
    joined = _utils.oxford_join(casings, last="or")
    current = (
        ''
        if not casings else
        f' Catalog is currently using {joined}.'
    )
    msg = (
        'snake_case field names are recommended for the greatest '
        f'compatibility with common big data technologies.{current}'
    )
    return _definitions.Critique('global', 'recommend_snake_case', msg)
