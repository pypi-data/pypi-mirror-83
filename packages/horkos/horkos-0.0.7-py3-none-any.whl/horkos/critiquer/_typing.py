import collections
import itertools
import typing

from horkos import cataloger
from horkos.critiquer import _definitions
from horkos.critiquer import _utils
from horkos import schemaomatic


@_utils.schema_not_in_catalog
def relative_type_consistency_check(
        schema: schemaomatic.Schema, catalog: cataloger.Catalog
) -> typing.Optional[_definitions.Critique]:
    """
    When comparing a schema against a catalog the schema's fields should have
    a typing consistent with the typing that already exists in the catalog.
    """
    fields = list(itertools.chain.from_iterable(
        schema.fields.values() for schema in catalog.schemas.values()
    ))
    type_map = collections.defaultdict(set)
    for field in fields:
        type_map[field.name].add(field.type_)
    errors = []
    for field in schema.fields.values():
        if field.name not in type_map or field.type_ in type_map[field.name]:
            continue
        types = list(sorted(type_map[field.name]))
        errors.append(
            (field.name, field.type_, _utils.oxford_join(types, last='or'))
        )
    if not errors:
        return None
    msg = '\n'.join(
        (
            f'{name} declared as {type_}, but other schemas in the catalog '
            f'have it declared as {types_str}. '
            f'The type of {name} should be consistent between schemas.'
        )
        for name, type_, types_str in errors
    )
    return _definitions.Critique('relative', 'type_consistency', msg)


def global_type_consistency_check(
        catalog: cataloger.Catalog
) -> typing.Optional[_definitions.Critique]:
    """
    Field types should be consistent within the catalog.

    :param catalog:
        The group of schemas to check for type uniformity.
    :return:
        A _definitions.Critique if one is found, otherwise nothing.
    """
    fields = list(itertools.chain.from_iterable(
        schema.fields.values() for schema in catalog.schemas.values()
    ))
    type_map = collections.defaultdict(set)
    for field in fields:
        type_map[field.name].add(field.type_)
    msg = '\n'.join(
        (
            f'Catalog describes {name} as '
            f'{_utils.oxford_join(list(sorted(types)))}. '
            f'The type of {name} should be consistent between schemas.'
        )
        for name, types in type_map.items()
        if len(types) > 1
    )
    if not msg:
        return None
    return _definitions.Critique('global', 'type_consistency', msg)
