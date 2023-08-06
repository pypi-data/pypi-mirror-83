import io
import typing

from horkos import schemaomatic


class Catalog:
    """A collection of schemas."""

    def __init__(
            self,
            schemas: typing.List[schemaomatic.Schemaable] = None,
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
            schemaomatic.load_schema(s, strict=strict) for s in schemas
        ]
        self.schemas = {s.name: s for s in all_schemas}

    def process(
            self,
            name: str,
            record: dict,
    ) -> dict:
        """
        Process a record, validating that it meets all the schema's checks.
        If it does not meet the requirements an exception is raised.

        :param name:
            The name of the data being processed. This is used to identify
            the schema to check the record against.
        :param record:
            The record to process.
        :return:
            The processed record with values cast and validated.
        """
        schema = self.schemas.get(name)
        if schema is None:
            raise ValueError(f'No schema exists for "{name}"')
        return schema.process(record)

    def update(self, schema: schemaomatic.Schemaable):
        """
        Update the catalog with the given schema.

        :param schema:
            The schema to add/update to the catalog.
        """
        to_add = schemaomatic.load_schema(schema, strict=self.strict)
        self.schemas[to_add.name] = to_add
