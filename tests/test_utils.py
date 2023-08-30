import pytest
import sys
import os

# set system path to ./src folder:
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from utils import convert_iso8601_to_unix_timestamp
from utils import load_config


def test_load_config():
    # Test case: Check if the function returns a dictionary
    assert isinstance(load_config(), dict)


# Test that the function correctly converts a valid ISO8601 timestamp to a Unix timestamp.
def test_valid_iso8601_timestamp():
    assert convert_iso8601_to_unix_timestamp("2020-01-01T00:00:00Z") == "1577836800"


# Test that the function handles an empty string input correctly.
def test_empty_string():
    try:
        convert_iso8601_to_unix_timestamp("")
    except ValueError:
        assert True
    else:
        assert False, "Expected ValueError was not raised."


# Test that the function handles a valid ISO8601 timestamp input that is not in UTC timezone correctly.
def test_valid_iso8601_timestamp_not_utc():
    assert (
        convert_iso8601_to_unix_timestamp("2020-01-01T00:00:00+01:00") == "1577833200"
    )
