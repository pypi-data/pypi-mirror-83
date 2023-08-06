import typing
import dataclasses

@dataclasses.dataclass(frozen=True)
class Field:
    """
    The definition of a field within a schema.

    :vartype name: str
    :ivar name:
        The name of the field.
    :vartype type_: str
    :ivar type_:
        The type of the field. Allowed values include: "boolean", "integer",
        "float", and "string".
    :vartype description: str
    :ivar description:
        A detailed description of the field.
    :vartype required: bool
    :ivar required:
        Whether the field is required to be present.
    :vartype required: bool
    :ivar nullable:
        Whether the field should accept null values.
    :vartype checks: list
    :ivar checks:
        A list of tuples, each tuple containing the name of a the check
        and a callable that can be used to evaluate the check.
    :vartype labels: dict
    :ivar labels:
        A space for unstructured information regarding the field.
    """

    name: str
    type_: str
    description: str
    required: bool
    nullable: bool
    checks: list
    labels: dict


@dataclasses.dataclass(frozen=True)
class Check:
    """
    The definition of a check within a field.

    :vartype name: str
    :ivar name:
        The name of the field.
    :vartype handler: typing.Callable
    :ivar handler:
        A callable object that processes a single value, returning True
        if the value passes the check or False if it fails.
    :vartype args: dict
    :ivar args:
        The arguments used to configure the handler.
    """

    name: str
    handler: typing.Callable
    args: dict
