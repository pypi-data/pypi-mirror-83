from unittest import mock

from horkos.critiquer import _typing


def test_catalog_type_consistency_check_with_critique():
    """The types of each field should be consistent across schemas."""
    field_1 = mock.MagicMock()
    field_1.name = 'foobar'
    field_1.type_ = 'string'
    field_2 = mock.MagicMock()
    field_2.name = 'foobar'
    field_2.type_ = 'integer'
    catalog = mock.MagicMock(
        schemas={
            'ds1': mock.MagicMock(fields={'foobar': field_1}),
            'ds2': mock.MagicMock(fields={'foobar': field_2}),
        }
    )

    result = _typing.catalog_type_consistency_check(catalog)

    assert result
    expected = (
        'Catalog describes foobar as integer and string. The type of foobar '
        'should be consistent between schemas.'
    )
    assert expected in result[0].message


def test_catalog_type_consistency_check_without_critique():
    """If types are consistent then no critique should be returned."""
    field_1 = mock.MagicMock()
    field_1.name = 'foobar'
    field_1.type_ = 'integer'
    field_2 = mock.MagicMock()
    field_2.name = 'foobar'
    field_2.type_ = 'integer'
    catalog = mock.MagicMock(
        schemas={
            'ds1': mock.MagicMock(fields={'foobar': field_1}),
            'ds2': mock.MagicMock(fields={'foobar': field_2}),
        }
    )

    result = _typing.catalog_type_consistency_check(catalog)

    assert not result


def test_relative_type_consistency_check_with_critique():
    """The types of a new schema should be consistent with existing"""
    existing_field = mock.MagicMock()
    existing_field.name = 'foobar'
    existing_field.type_ = 'integer'
    existing_schema = mock.MagicMock()
    existing_schema.fields = {'foobar': existing_field}
    catalog = mock.MagicMock(schemas={'ds1': existing_schema})
    new_field = mock.MagicMock()
    new_field.name = 'foobar'
    new_field.type_ = 'string'
    new_schema = mock.MagicMock()
    new_schema.fields = {'foobar': new_field}

    result = _typing.relative_type_consistency_check(new_schema, catalog)

    assert result
    expected = 'other schemas in the catalog have it declared as integer'
    assert expected in result[0].message


def test_relative_type_consistency_check_without_critique():
    """If types are consistent, then no critiques should be raised."""
    existing_field = mock.MagicMock()
    existing_field.name = 'foobar'
    existing_field.type_ = 'integer'
    existing_schema = mock.MagicMock()
    existing_schema.fields = {'foobar': existing_field}
    catalog = mock.MagicMock(schemas={'ds1': existing_schema})
    new_field = mock.MagicMock()
    new_field.name = 'foobar'
    new_field.type_ = 'integer'
    new_schema = mock.MagicMock()
    new_schema.fields = {'foobar': new_field}

    result = _typing.relative_type_consistency_check(new_schema, catalog)

    assert not result
