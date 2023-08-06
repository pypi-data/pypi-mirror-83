from unittest import mock

import pytest

from horkos.critiquer import _casing


def test_local_uniform_field_casing_check_with_critique():
    """Should identify mixed casing conventions within schema"""
    schema = mock.MagicMock()
    schema.fields = {
        'fooBar': 'something',
        'fiz_buzz': 'something',
    }

    result = _casing.local_uniform_field_casing_check(schema)

    expected = 'camelCase and snake_case are most common with 1 matching.'
    assert expected in result.message


def test_local_uniform_field_casing_check_without_critique():
    """Should return none if the casing is consistent"""
    schema = mock.MagicMock()
    schema.fields = {
        'foobar': 'something',
        'fiz_buzz': 'something',
    }

    result = _casing.local_uniform_field_casing_check(schema)

    assert result is None


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

    expected = (
        r'60% of fields in the catalog follow snake_case. '
        'Among new fields the dominant convention is camelCase'
    )
    assert expected in result.message


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

    assert result is None


def test_global_field_casing_check_with_critique():
    """Should be able to identify inconsistent naming in a catalog of data."""
    catalog = mock.MagicMock(
        schemas={
            'foo': mock.MagicMock(fields={'fooBar': None, 'fiz_buzz': None}),
            'baz': mock.MagicMock(
                fields={'fooBar': None, 'boo_far': None, 'biz_fuzz': None}
            ),
        }
    )

    result = _casing.global_field_casing_check(catalog)

    expected = (
        'No clear casing convention. snake_case is most '
        'common with 60% matching.'
    )
    assert expected in result.message


def test_global_field_casing_check_without_critique():
    """Should return None if all fields are consistent."""
    catalog = mock.MagicMock(
        schemas={
            'foo': mock.MagicMock(fields={'foobar': None, 'fiz_buzz': None}),
            'baz': mock.MagicMock(
                fields={'foobar': None, 'boo_far': None, 'biz_fuzz': None}
            ),
        }
    )

    result = _casing.global_field_casing_check(catalog)

    assert result is None


def test_local_prefer_snake_case_with_critique():
    """
    Should be able to identify when snake_case isn't used in a schema
    and recommend its usage.
    """
    schema = mock.MagicMock(fields={'fooBar': None, 'bizFuzz': None})

    result = _casing.local_prefer_snake_case(schema)

    expected = 'snake_case field names are recommended'
    assert expected in result.message


def test_local_prefer_snake_case_without_critique():
    """If snake_case is already used, then return None."""
    schema = mock.MagicMock(fields={'foobar': None, 'fiz_buzz': None})

    result = _casing.local_prefer_snake_case(schema)

    assert result is None


def test_global_prefer_snake_case_with_critique():
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

    result = _casing.global_prefer_snake_case(catalog)

    expected = 'snake_case field names are recommended'
    assert expected in result.message


def test_global_prefer_snake_case_without_critique():
    """If snake_case is already used, then return None."""
    catalog = mock.MagicMock(
        schemas={
            'foo': mock.MagicMock(fields={'foobar': None, 'fiz_buzz': None}),
            'baz': mock.MagicMock(
                fields={'foobar': None, 'boo_far': None, 'biz_fuzz': None}
            ),
        }
    )

    result = _casing.global_prefer_snake_case(catalog)

    assert result is None
