import typing


class Field(typing.NamedTuple):
    """The schema of a specific field in the dataset."""

    name: str
    type_: str
    description: str
    required: bool
    nullable: bool
    checks: typing.Dict[str, typing.Callable]
    labels: list
