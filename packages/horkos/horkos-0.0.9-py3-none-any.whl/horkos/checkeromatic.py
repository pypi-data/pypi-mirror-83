import datetime
import json
import re
import functools
import typing


def _unhandled_exceptions_return(return_value: bool) -> typing.Callable:
    """
    Create a decorator that converts all unhandled exceptions to the given
    return value.
    """

    def decorator(func: typing.Callable) -> typing.Callable:
        """Decorate the given input function."""

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """
            Convert all non keyboard interupt exceptions to the given
            value
            """
            try:
                return func(*args, **kwargs)
            except KeyboardInterrupt as err:
                raise err
            except Exception as err:
                return return_value
        return wrapper

    return decorator


class JsonStringChecker():
    """Checker for validating that a string is json deserializable."""

    name = 'json'

    @_unhandled_exceptions_return(False)
    def __call__(self, value: typing.Any) -> bool:
        """Confirm the given value can be deserialized to json."""
        json.loads(value)
        return True


class JsonArrayStringChecker():
    """
    Checker for validating that a string is json deserializable and
    deserializes into an array.
    """

    name = 'json_array'

    @_unhandled_exceptions_return(False)
    def __call__(self, value: typing.Any) -> bool:
        """Confirm the given value can be json deserialized to an array."""
        result = json.loads(value)
        return isinstance(result, list)


class JsonObjectStringChecker():
    """
    Checker for validating that a string is json deserializable and
    deserializes into an object.
    """

    name = 'json_object'

    @_unhandled_exceptions_return(False)
    def __call__(self, value: typing.Any) -> bool:
        """Confirm the given value can be json deserialized to an object."""
        result = json.loads(value)
        return isinstance(result, dict)


class ChoiceChecker():
    """Checker for validating that a value is in a set of choices."""

    name = 'choice'

    def __init__(self, options: list = None):
        self._options = set(options)

    @_unhandled_exceptions_return(False)
    def __call__(self, value: typing.Any) -> bool:
        """Confirm the given value is a valid choice"""
        return value in self._options


class IsoTimestampChecker():
    """Checker for validating that a value is an iso timestamp."""

    name = 'iso_timestamp'

    @_unhandled_exceptions_return(False)
    def __call__(self, value: typing.Any) -> bool:
        """Confirm the given value is a valid iso timestamp."""
        datetime.datetime.fromisoformat(value)
        return True


class MaxChecker():
    """Checker for validating that a value is less than a given value."""

    name = 'maximum'

    def __init__(
            self, limit: typing.Union[str, int, float], inclusive: bool = True
    ):
        """
        Initialize the checker with its configured values.

        :param limit:
            The maximum value to allow.
        :param inclusive:
            Whether to allow the input value to be be exactly the limit or
            if the limit should be exclusive.
        """
        self._limit = limit
        self._inclusive = inclusive

    @_unhandled_exceptions_return(False)
    def __call__(self, value: typing.Any) -> bool:
        """Confirm that a given value is less than the specified limit."""
        return value <= self._limit if self._inclusive else value < self._limit


class MinChecker():
    """Checker for validating that a value is greater than a given value."""

    name = 'minimum'

    def __init__(
            self, limit: typing.Union[str, int, float], inclusive: bool = True
    ):
        """
        Initialize the checker with its configured values.

        :param limit:
            The minimum value to allow.
        :param inclusive:
            Whether to allow the input value to be be exactly the limit or
            if the limit should be exclusive.
        """
        self._limit = limit
        self._inclusive = inclusive

    @_unhandled_exceptions_return(False)
    def __call__(self, value: typing.Any) -> bool:
        """Confirm that a given value is greater than the specified limit."""
        return value >= self._limit if self._inclusive else value > self._limit


class RegexChecker():
    """Checker for validating that a value meets the given regex."""

    name = 'regex'

    def __init__(self, regex: str = None, ignore_case=False):
        flags = re.IGNORECASE if ignore_case else 0
        self._regex = re.compile(regex, flags)

    @_unhandled_exceptions_return(False)
    def __call__(self, value: typing.Any) -> bool:
        """Confirm the given value matches the regex."""
        return bool(self._regex.match(value))


class EmailChecker(RegexChecker):
    """Checker for validating that a value is a valid email."""

    name = 'email'

    def __init__(self):
        super().__init__(
            regex=r'^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,63}$',
            ignore_case=True
        )


class UuidChecker(RegexChecker):
    """Checker for validating that a value is a valid email."""

    name = 'uuid'

    def __init__(self):
        pat = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        super().__init__(regex=pat, ignore_case=True)


CHECKERS = [
    ChoiceChecker,
    EmailChecker,
    IsoTimestampChecker,
    JsonArrayStringChecker,
    JsonObjectStringChecker,
    JsonStringChecker,
    MaxChecker,
    MinChecker,
    RegexChecker,
    UuidChecker,
]
CHECKER_MAP = {c.name: c for c in CHECKERS}
