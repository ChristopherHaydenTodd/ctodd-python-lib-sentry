#!/usr/bin/env python3
"""
    Purpose:
        Helper Library for Sentry. Will provide a functions for connecting to
        Sentry and logging events to Sentry
"""

# Python Library Imports
import os
import logging
import raven


###
# Sentry Functions
###


def log_to_sentry(sentry_host, sentry_port, sentry_key, sentry_db):
    """
    Purpose:
        Logs Exception to Sentry if in production enviornment tier. if
        the environment is any other tier, it will not send to sentry.
    Args:
        sentry_host (String): Host of Sentry Service
        sentry_port (Int): Port of Sentry Service
        sentry_key (String): Key for Sentry Service
        sentry_db (Int): Which endpoint to log sentry objects to
    Returns:
        event_id (string): ID of the event being created in Sentry
    """

    event_id = None

    env_tier = os.environ.get("ENV_TIER", "dev")
    if env_tier in ("prod", "production"):
        sentry_client = connect_to_sentry(
            sentry_host, sentry_port, sentry_key, sentry_db
        )
        if sentry_client:
            event_id = sentry_client.captureException()
        else:
            logging.error("Could not get sentry client")
    else:
        logging.error(f"Not Logging to Sentry, In {env_tier} Environment")

    return event_id


def connect_to_sentry(sentry_host, sentry_port, sentry_key, sentry_db):
    """
    Purpose:
        Connects to Sentry and returns connection
    Args:
        sentry_host (String): Host of Sentry Service
        sentry_port (Int): Port of Sentry Service
        sentry_key (String): Key for Sentry Service
        sentry_db (Int): Which endpoint to log sentry objects to
    Returns:
        sentry_client (Client: Client connection to Sentry
    """

    sentry_url = f"https://{sentry_key}@{sentry_host}:{sentry_port}/{sentry_db}"
    try:
        return raven.Client(
            dsn=sentry_url,
            auto_log_stacks=True,
            include_paths=[__name__.split(".", 1)[0]],
            sample_rate=1,
        )
    except Exception as err:
        logging.error("Error Connecting to Sentry: {0}".format(err))
