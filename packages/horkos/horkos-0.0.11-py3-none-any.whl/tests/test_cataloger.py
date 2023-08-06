import pytest

from horkos import cataloger


def test_catalog_process_happy_path():
    """Should be able to process a record through a catalog."""
    schema = {
        'name': 'dataset',
        'fields': {'foo': {'type': 'string'}}
    }
    catalog = cataloger.Catalog([schema], strict=False)

    record = catalog.process('dataset', {'foo': 'bar'})

    assert record['foo'] == 'bar'


def test_catalog_process_sad_path():
    """Should be able to process a record through a catalog."""
    catalog = cataloger.Catalog()

    with pytest.raises(ValueError) as err:
        catalog.process('doesnt-exist', {'foo': 'bar'})

    assert 'No schema exists for "doesnt-exist"' in str(err.value)


def test_catalog_update():
    """Should be able to update an existing catalog."""
    catalog = cataloger.Catalog(strict=False)
    schema = {
        'name': 'dataset',
        'fields': {'foo': {'type': 'string'}}
    }
    catalog.update(schema)

    record = catalog.process('dataset', {'foo': 'bar'})

    assert record['foo'] == 'bar'
