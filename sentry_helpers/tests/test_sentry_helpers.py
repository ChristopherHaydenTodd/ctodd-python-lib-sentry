#!/usr/bin/env python3
"""
    Purpose:
        Test File for sentry_helpers.py
"""

# Python Library Imports
import os
import sys
import pytest
from raven import Client
from unittest import mock

# Import File to Test
BASE_PROJECT_PATH = f"{os.path.dirname(os.path.realpath(__file__))}/../"
sys.path.insert(0, BASE_PROJECT_PATH)
import sentry_helpers


###
# Fixtures
###


@pytest.fixture
def example_host():
    """
    Purpose:
        Set example host for sentry
    Args:
        N/A
    Return:
        example_host (Pytest Fixture (String)): example host for sentry
    """

    return "sentry_host"


@pytest.fixture
def example_port():
    """
    Purpose:
        Set example port for sentry
    Args:
        N/A
    Return:
        example_port (Pytest Fixture (Int)): example port for sentry
    """

    return 21212


@pytest.fixture
def example_key():
    """
    Purpose:
        Set example key for sentry
    Args:
        N/A
    Return:
        example_key (Pytest Fixture (String)): example key for sentry
    """

    return "sentry_key"


@pytest.fixture
def example_db():
    """
    Purpose:
        Set example db for sentry
    Args:
        N/A
    Return:
        example_db (Pytest Fixture (Int)): example db for sentry
    """

    return 17


@pytest.fixture
def example_event():
    """
    Purpose:
        Set example event for sentry
    Args:
        N/A
    Return:
        example_event (Pytest Fixture (String)): example event from sentry
    """

    return "some_event"


###
# Mocked Functions
###


class MockClient(object):
    """
    Purpose:
        Mock a Sentry Client Call
    """

    def __init__(
        self, dsn=None, auto_log_stacks=None, include_paths=None, sample_rate=None
    ):
        """
        Purpose:
            Initialize the MockClient Object
        """

        self.dsn = dsn
        self.auto_log_stacks = auto_log_stacks
        self.include_paths = include_paths
        self.sample_rate = sample_rate

    def captureException(self):
        """
            Mock the captureException of Client which is called
        """

        pass


###
# Test Logging to Sentry
###


@mock.patch("raven.Client", autospec=MockClient)
def test_log_to_sentry_prod_env(
    mocked_class, example_host, example_port, example_key, example_db, example_event
):
    """
    Purpose:
        Tests that a sentry alert is logged when in a production environment
    Args:
        mocked_class (Mocked Class): Mocked version of raven.Client
        example_host (Pytest Fixture (String)): example host for sentry
        example_port (Pytest Fixture (Int)): example port for sentry
        example_key (Pytest Fixture (String)): example key for sentry
        example_db (Pytest Fixture (Int)): example db for sentry
        example_event (Pytest Fixture (String)): example event from sentry
    Return:
        N/A
    """

    # Set event Return
    mocked_class.captureException.return_value = example_event
    expected_event = example_event

    # Setting Environment
    os.environ["ENV_TIER"] = "prod"

    # Calling Tested Method
    event_id = sentry_helpers.log_to_sentry(
        example_host, example_port, example_key, example_db
    )

    # Assertions
    mocked_class.assert_called()
    assert mocked_class.called
    assert mocked_class.call_count == 1
    # assert event_id == expected_event


@mock.patch("raven.Client", autospec=MockClient)
def test_log_to_sentry_non_prod_env(
    mocked_class, example_host, example_port, example_key, example_db
):
    """
    Purpose:
        Tests that a sentry alert is NOT logged in a non-production environment
    Args:
        mocked_class (Mocked Class): Mocked version of raven.Client
    Return:
        N/A
    """

    # Setting Environment
    os.environ["ENV_TIER"] = "dev"

    # Calling Tested Method
    event_id = sentry_helpers.log_to_sentry(
        example_host, example_port, example_key, example_db
    )

    # Assertions
    mocked_class.assert_not_called()
    assert not mocked_class.called
    assert mocked_class.call_count == 0
    assert event_id is None


@mock.patch("raven.Client", autospec=MockClient)
def test_log_to_sentry_env_tier_not_set(
    mocked_class, example_host, example_port, example_key, example_db
):
    """
    Purpose:
        Tests that a sentry alert is NOT logged in an unidentified environment
    Args:
        mocked_class (Mocked Class): Mocked version of raven.Client
    Return:
        N/A
    """

    # Setting Environment
    del os.environ["ENV_TIER"]

    # Calling Tested Method
    event_id = sentry_helpers.log_to_sentry(
        example_host, example_port, example_key, example_db
    )

    # Assertions
    mocked_class.assert_not_called()
    assert not mocked_class.called
    assert mocked_class.call_count == 0
    assert event_id is None
