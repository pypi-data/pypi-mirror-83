import io
import typing

from horkos import _schemaomatic


class Catalog:
    """
    A collection of schemas.

    :vartype schemas: typing.Dict[str, horkos.Schema]
    :ivar schemas:
        All of the schemas in the catalog.
    """

    def __init__(
            self,
            schemas: typing.List[_schemaomatic.Schemaable] = None,
            strict: bool = True,
    ):
        """
        Initialize the catalog of data schemas.

        :param schema_files:
            Yaml file paths of schema files to include in the catalog.
        :param schemas:
            Existing schema objects to include in the catalog.
        :param strict:
            Whether to operate in strict mode. If True descriptions will be
            required.
        """
        self.strict = strict
        schemas = schemas or []
        all_schemas = [
            _schemaomatic.load_schema(s, strict=strict) for s in schemas
        ]
        self.schemas = {s.name: s for s in all_schemas}

    def cast(self, name: str, record: dict) -> dict:
        """
        Cast the fields of the record to the types described in its schema.
        All undeclared fields will be removed from the record.

        :param name:
            The name of the schema associated with the record.
        :param record:
            The record to cast using the schema. This is expected to be
            a dictionary mapping field names to field values.
        :return:
            The record with values cast to the correct types.
        """
        schema = self._pull_schema(name)
        return schema.cast(record)

    def find_errors(self, name: str, record: dict) -> list:
        """
        Identify any failed checks for the given record.

        Run all field checks against the record, identifying all failed
        checks. Returns a list of errors if any of the checks have failed
        or an empty list if all passed.

        :param name:
            The name of the schema associated with the record.
        :param record:
            The record to inspect for errors.
        :return:
            A list of errors associated with the record.
        """
        schema = self._pull_schema(name)
        return schema.find_errors(record)

    def process(
            self,
            name: str,
            record: dict,
    ) -> dict:
        """
        Process a record against a named schema from the catalog.

        Each field within the record will be cast to the type specified in
        the schema and the resulting value validated against the checks
        defined within the schema. If any of the fields
        cannot be successfully cast or any of the checks fail a
        RecordValidationError exception will be raised.

        :param name:
            The name of the schema to process the record against.
        :param record:
            The record to process against the schema. This should be
            a dictionary mapping field names to field values.
        :return:
            The processed record with values cast and validated.
        """
        schema = self._pull_schema(name)
        return schema.process(record)

    def _pull_schema(self, name: str) -> _schemaomatic.Schema:
        """
        Pull the schema with the given name, if no matching schema exists
        raise a value error indicating as much.
        """
        schema = self.schemas.get(name)
        if schema is None:
            raise ValueError(f'No schema exists for "{name}"')
        return schema

    def update(self, schema: _schemaomatic.Schemaable):
        """
        Update the catalog with the given schema.

        :param schema:
            The schema to add/update to the catalog.
        """
        to_add = _schemaomatic.load_schema(schema, strict=self.strict)
        self.schemas[to_add.name] = to_add
