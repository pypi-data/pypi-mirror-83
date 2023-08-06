import typing


class Critique(typing.NamedTuple):
    """A critique of a dataschema."""

    scope: str
    code: str
    message: str
    schema_name: str = None
    field_name: str = None

    def __str__(self):
        """Convert the critique to a string."""
        parts = [self.schema_name, self.field_name]
        parts = [p for p in parts if p is not None]
        name = '.'.join(parts)
        return f'[{self.code}] {name} - {self.message}'
