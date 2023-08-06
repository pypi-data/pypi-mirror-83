import pytest

from horkos import casters
from horkos import definitions
from horkos import errors


def test_cast_happy_path():
    """Should be able to cast each of a records values to its expected type."""
    bool_field = definitions.Field(
        name='bool_field',
        type_='boolean',
        description='Some description',
        required=True,
        nullable=False,
        checks={},
        labels={},
    )
    field_map = {
        'bool_field_1': bool_field._replace(name='bool_field_1'),
        'bool_field_2': bool_field._replace(name='bool_field_2'),
        'bool_field_3': bool_field._replace(name='bool_field_3'),
        'bool_field_4': bool_field._replace(name='bool_field_4'),
        'bool_field_5': bool_field._replace(name='bool_field_5'),
        'int_field': definitions.Field(
            name='int_field',
            type_='integer',
            description='Some description',
            required=True,
            nullable=False,
            checks={},
            labels={},
        ),
        'str_field': definitions.Field(
            name='str_field',
            type_='string',
            description='Some description',
            required=True,
            nullable=False,
            checks={},
            labels={},
        ),
    }
    record = {
        'bool_field_1': 'true',
        'bool_field_2': 'False',
        'bool_field_3': 1,
        'bool_field_4': 0,
        'bool_field_5': True,
        'int_field': '123',
        'str_field': 12345
    }

    cast = casters.cast(record, field_map)

    assert cast['bool_field_1'] is True
    assert cast['bool_field_2'] is False
    assert cast['bool_field_3'] is True
    assert cast['bool_field_4'] is False
    assert cast['bool_field_5'] is True
    assert cast['int_field'] == 123
    assert cast['str_field'] == '12345'


def test_cast_raises_all_errors():
    """Should raise all errors when present."""
    field_map = {
        'bool_field': definitions.Field(
            name='bool_field',
            type_='boolean',
            description='Some description',
            required=True,
            nullable=False,
            checks={},
            labels={},
        ),
        'float_field': definitions.Field(
            name='float_field',
            type_='float',
            description='Some description',
            required=True,
            nullable=False,
            checks={},
            labels={},
        ),
        'int_field_1': definitions.Field(
            name='int_field_1',
            type_='integer',
            description='Some description',
            required=True,
            nullable=False,
            checks={},
            labels={},
        ),
        'int_field_2': definitions.Field(
            name='int_field_2',
            type_='integer',
            description='Some description',
            required=True,
            nullable=False,
            checks={},
            labels={},
        ),
        'str_field_1': definitions.Field(
            name='str_field_1',
            type_='string',
            description='Some description',
            required=True,
            nullable=False,
            checks={},
            labels={},
        ),
        'str_field_2': definitions.Field(
            name='str_field_2',
            type_='string',
            description='Some description',
            required=True,
            nullable=False,
            checks={},
            labels={},
        ),
    }
    record = {
        'bool_field': 'T',
        'float_field': 'word',
        'int_field_1': 1.123,
        'int_field_2': 'word',
        'str_field_1': None,
    }

    with pytest.raises(errors.RecordValidationError) as err:
        casters.cast(record, field_map)

    msg = 'value of "T" for bool_field could not be cast to boolean'
    assert msg in str(err.value)
    msg = 'value of "word" for float_field could not be cast to float'
    assert msg in str(err.value)
    msg = 'value of "1.123" for int_field_1 could not be cast to integer'
    assert msg in str(err.value)
    msg = 'value of "word" for int_field_2 could not be cast to integer'
    assert msg in str(err.value)
    msg = 'str_field_1 cannot be null'
    assert msg in str(err.value)
    msg = 'str_field_2 is required'
    assert msg in str(err.value)
