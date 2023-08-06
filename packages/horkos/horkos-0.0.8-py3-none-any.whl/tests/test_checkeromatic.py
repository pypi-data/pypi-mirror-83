import json
from unittest import mock
import uuid

import pytest

from horkos import checkeromatic


def test_json_string_checker_happy_path():
    """Should be able check a valid json string."""
    value = json.dumps({'foo': 'bar'})
    checker = checkeromatic.JsonStringChecker()

    passes = checker(value)

    assert passes


def test_json_string_checker_bad_json():
    """Should be able check an invalid json string."""
    checker = checkeromatic.JsonStringChecker()

    passes = checker('<xml></xml>')

    assert not passes


def test_json_string_checker_wrong_type():
    """Should be able check a value of the wrong type."""
    checker = checkeromatic.JsonStringChecker()

    passes = checker(12)

    assert not passes


def test_choice_checker_happy_path():
    """
    Should be able to check that a value is within a valid set of
    choices.
    """
    checker = checkeromatic.ChoiceChecker(options=['foo', 'bar'])

    passes = checker('foo')

    assert passes


def test_choice_checker_bad_value():
    """
    Should be able to see that a value is not within a valid set of
    choices.
    """
    checker = checkeromatic.ChoiceChecker(options=['foo', 'bar'])

    passes = checker('fizbuzz')

    assert not passes


def test_email_checker_happy_path():
    """Should be able to validate an email."""
    checker = checkeromatic.EmailChecker()

    passes = checker('could.be@an-email.com')

    assert passes


def test_email_checker_bad_value():
    """Should be able to identify an invalid email."""
    checker = checkeromatic.EmailChecker()

    passes = checker('for-sure-not-valid')

    assert not passes


def test_uuid_checker_happy_path():
    """Should be able to validate a uuid."""
    value = str(uuid.uuid4())
    checker = checkeromatic.UuidChecker()

    passes = checker(value)

    assert passes


def test_uuid_checker_bad_value():
    """Should be able to identify a non-uuid."""
    value = '398l159z-8m4n-455o-pqr0-75s66tu074jk'
    checker = checkeromatic.UuidChecker()

    passes = checker(value)

    assert not passes


def test_iso_timestamp_checker_happy_path():
    """Should be able to identify a iso compliant timestamp."""
    value = '2020-03-18T12:34:56'
    checker = checkeromatic.IsoTimestampChecker()

    passes = checker(value)

    assert passes


@mock.patch('json.loads')
def test_keyboard_interupts_surface(loads: mock.MagicMock):
    """A keyboard interupt should always get reraised."""
    loads.side_effect = KeyboardInterrupt
    checker = checkeromatic.JsonStringChecker()

    with pytest.raises(KeyboardInterrupt):
        checker('some-value')
