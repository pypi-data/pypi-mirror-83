from unittest import mock

import pytest

from horkos import critiquer


def test_schema_uniform_field_casing_check_with_critique():
    """Should identify mixed casing conventions within schema"""
    schema = mock.MagicMock()
    schema.fields = {
        'fooBar': 'something',
        'fiz_buzz': 'something',
    }

    result = critiquer.schema_uniform_field_casing_check(schema)

    expected = 'camelCase and snake_case are most common with 1 matching.'
    assert expected in result.message


def test_schema_uniform_field_casing_check_without_critique():
    """Should return none if the casing is consistent"""
    schema = mock.MagicMock()
    schema.fields = {
        'foobar': 'something',
        'fiz_buzz': 'something',
    }

    result = critiquer.schema_uniform_field_casing_check(schema)

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

    result = critiquer.relative_field_casing_check(schema, catalog)

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
        critiquer.relative_field_casing_check(schema, catalog)


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

    result = critiquer.relative_field_casing_check(schema, catalog)

    assert result is None


def test_oxford_join_empty_list():
    """
    When turning an empty list into a string we should get an empty
    string.
    """
    result = critiquer._oxford_join([])

    assert result == ''
