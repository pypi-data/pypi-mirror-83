import typing


class Critique(typing.NamedTuple):
    """A critique of a dataschema."""

    scope: str
    code: str
    message: str
