from unittest import mock

import pytest

from horkos.critiquer import _casing


def test_schema_uniform_field_casing_check_with_critique():
    """Should identify mixed casing conventions within schema"""
    schema = mock.MagicMock()
    schema.fields = {
        'fooBar': 'something',
        'fiz_buzz': 'something',
    }

    result = _casing.schema_uniform_field_casing_check(schema)

    assert result
    expected = 'camelCase and snake_case are most common with 1 matching.'
    assert expected in result[0].message


def test_schema_uniform_field_casing_check_without_critique():
    """Should return none if the casing is consistent"""
    schema = mock.MagicMock()
    schema.fields = {
        'foobar': 'something',
        'fiz_buzz': 'something',
    }

    result = _casing.schema_uniform_field_casing_check(schema)

    assert not result


def test_relative_field_casing_check_with_critique():
    """Should identify mixed field conventions between schema and catalog."""
    catalog = mock.MagicMock(
        schemas={
            'foo': mock.MagicMock(fields={'fooBar': None, 'fiz_buzz': None}),
            'baz': mock.MagicMock(
                fields={'fooBar': None, 'boo_far': None, 'biz_fuzz': None}
            ),
        }
    )
    schema = mock.MagicMock(fields={'fooBar': None, 'bizFuzz': None})

    result = _casing.relative_field_casing_check(schema, catalog)

    assert result
    expected = (
        'The casing of bizFuzz does not match the dominant patterns of the '
        'catalog'
    )
    assert expected in result[0].message


def test_relative_field_casing_check_with_schema_in_catalog():
    """If the schema is already in the catalog an error should be raised."""
    catalog = mock.MagicMock(schemas={'foo': 'bar'})
    schema = mock.MagicMock()
    schema.name = 'foo'

    with pytest.raises(ValueError):
        _casing.relative_field_casing_check(schema, catalog)


def test_relative_field_casing_without_critique():
    """Should return None if their are no issues."""
    catalog = mock.MagicMock(
        schemas={
            'foo': mock.MagicMock(fields={'fooBar': None, 'fizBuzz': None}),
            'baz': mock.MagicMock(
                fields={'fooBar': None, 'booFar': None, 'bizFuzz': None}
            ),
        }
    )
    schema = mock.MagicMock(fields={'fooBar': None, 'bizFuzz': None})

    result = _casing.relative_field_casing_check(schema, catalog)

    assert not result


def test_catalog_field_casing_check_with_critique():
    """Should be able to identify inconsistent naming in a catalog of data."""
    catalog = mock.MagicMock(
        schemas={
            'foo': mock.MagicMock(fields={'fooBar': None, 'fiz_buzz': None}),
            'baz': mock.MagicMock(
                fields={'fooBar': None, 'boo_far': None, 'biz_fuzz': None}
            ),
        }
    )

    result = _casing.catalog_field_casing_check(catalog)

    assert result
    expected = (
        'No clear casing convention. snake_case is most '
        'common with 60% matching.'
    )
    assert expected in result[0].message


def test_catalog_field_casing_check_without_critique():
    """Should return None if all fields are consistent."""
    catalog = mock.MagicMock(
        schemas={
            'foo': mock.MagicMock(fields={'foobar': None, 'fiz_buzz': None}),
            'baz': mock.MagicMock(
                fields={'foobar': None, 'boo_far': None, 'biz_fuzz': None}
            ),
        }
    )

    result = _casing.catalog_field_casing_check(catalog)

    assert not result


def test_schema_prefer_snake_case_with_critique():
    """
    Should be able to identify when snake_case isn't used in a schema
    and recommend its usage.
    """
    schema = mock.MagicMock(fields={'fooBar': None, 'bizFuzz': None})

    result = _casing.schema_prefer_snake_case(schema)

    assert result
    expected = 'snake_case field names are recommended'
    assert expected in result[0].message


def test_schema_prefer_snake_case_without_critique():
    """If snake_case is already used, then return None."""
    schema = mock.MagicMock(fields={'foobar': None, 'fiz_buzz': None})

    result = _casing.schema_prefer_snake_case(schema)

    assert not result


def test_catalog_prefer_snake_case_with_critique():
    """
    Should be able to identify when snake_case isn't used in a schema
    and recommend its usage.
    """
    catalog = mock.MagicMock(
        schemas={
            'foo': mock.MagicMock(fields={'Foobar': None, 'fiz_buzz': None}),
            'baz': mock.MagicMock(
                fields={'Foobar': None, 'BooFar': None, 'biz_fuzz': None}
            ),
        }
    )

    result = _casing.catalog_prefer_snake_case(catalog)

    assert result
    expected = 'snake_case field names are recommended'
    assert expected in result[0].message


def test_catalog_prefer_snake_case_without_critique():
    """If snake_case is already used, then return None."""
    catalog = mock.MagicMock(
        schemas={
            'foo': mock.MagicMock(fields={'foobar': None, 'fiz_buzz': None}),
            'baz': mock.MagicMock(
                fields={'foobar': None, 'boo_far': None, 'biz_fuzz': None}
            ),
        }
    )

    result = _casing.catalog_prefer_snake_case(catalog)

    assert not result
