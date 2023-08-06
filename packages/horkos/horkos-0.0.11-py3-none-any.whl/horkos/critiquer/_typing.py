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
) -> typing.List[_definitions.Critique]:
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
    critiques = []
    for field in schema.fields.values():
        if field.name not in type_map or field.type_ in type_map[field.name]:
            continue
        types = list(sorted(type_map[field.name]))
        types_str = _utils.oxford_join(types, last='or')
        msg = (
            f'{field.name} declared as {field.type_}, but other schemas in '
            f'the catalog have it declared as {types_str}. '
            f'The type of {field.name} should be consistent between schemas.'
        )
        critiques.append(_definitions.Critique(
            'relative', 'type_consistency', msg, schema.name, field.name
        ))
    return critiques

def catalog_type_consistency_check(
        catalog: cataloger.Catalog
) -> typing.List[_definitions.Critique]:
    """
    Field types should be consistent within the catalog.

    :param catalog:
        The group of schemas to check for type uniformity.
    :return:
        A list of _definitions.Critiques .
    """
    fields = list(itertools.chain.from_iterable(
        schema.fields.values() for schema in catalog.schemas.values()
    ))
    type_map = collections.defaultdict(set)
    for field in fields:
        type_map[field.name].add(field.type_)
    return [
        _definitions.Critique(
            'catalog',
            'type_consistency',
            (
                f'Catalog describes {field.name} as '
                f'{_utils.oxford_join(list(sorted(type_map[field.name])))}. '
                f'The type of {field.name} should be consistent between '
                'schemas.'
            ),
            schema.name,
            field.name
        )
        for schema in catalog.schemas.values()
        for field in schema.fields.values()
        if len(type_map[field.name]) > 1
    ]
