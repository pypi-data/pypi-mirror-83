import io
import os
from unittest import mock

from horkos import cmdline

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
RESOURCE_PATH = os.path.join(DIR_PATH, 'resources')


def test_check_cmdline():
    """Check cmdline should be able to run."""
    schema_file = os.path.join(RESOURCE_PATH, 'sample.yaml')
    data_file = os.path.join(RESOURCE_PATH, 'sample.csv')
    output = io.StringIO()

    with mock.patch('sys.stdout', new=output):
        cmdline.main(['check', '--schema', schema_file, data_file])

    result = output.getvalue()
    assert 'value of "ERROR" in method did not pass choice check' in result
    expected = 'value of "BAD" for response_code could not be cast to integer'
    assert expected in result
    assert '2 errors found' in result
