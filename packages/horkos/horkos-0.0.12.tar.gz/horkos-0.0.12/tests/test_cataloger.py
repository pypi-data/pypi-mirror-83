import pytest

from horkos import _cataloger


def test_catalog_process_happy_path():
    """Should be able to process a record through a catalog."""
    schema = {
        'name': 'dataset',
        'fields': {'foo': {'type': 'string'}}
    }
    catalog = _cataloger.Catalog([schema], strict=False)

    record = catalog.process('dataset', {'foo': 'bar'})

    assert record['foo'] == 'bar'


def test_catalog_process_sad_path():
    """Should be able to process a record through a catalog."""
    catalog = _cataloger.Catalog()

    with pytest.raises(ValueError) as err:
        catalog.process('doesnt-exist', {'foo': 'bar'})

    assert 'No schema exists for "doesnt-exist"' in str(err.value)


def test_catalog_cast_happy_path():
    """Should be able to cast a record through a catalog."""
    schema = {
        'name': 'dataset',
        'fields': {'foo': {'type': 'string'}}
    }
    catalog = _cataloger.Catalog([schema], strict=False)

    record = catalog.cast('dataset', {'foo': 123})

    assert record['foo'] == '123'


def test_catalog_find_errors_happy_path():
    """Should be able to find errors for a record through a catalog."""
    schema = {
        'name': 'dataset',
        'fields': {'foo': {'type': 'string'}}
    }
    catalog = _cataloger.Catalog([schema], strict=False)

    errors = catalog.find_errors('dataset', {'foo': 123})

    assert not errors


def test_catalog_update():
    """Should be able to update an existing catalog."""
    catalog = _cataloger.Catalog(strict=False)
    schema = {
        'name': 'dataset',
        'fields': {'foo': {'type': 'string'}}
    }
    catalog.update(schema)

    record = catalog.process('dataset', {'foo': 'bar'})

    assert record['foo'] == 'bar'
