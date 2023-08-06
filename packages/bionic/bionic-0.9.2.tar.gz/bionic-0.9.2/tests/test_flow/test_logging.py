import re

import pytest

import logging
import threading
import bionic as bn


class LogChecker:
    def __init__(self, caplog):
        self._caplog = caplog

    def expect_all(self, *expected_messages):
        actual_messages = self._pop_messages()
        assert set(actual_messages) == set(expected_messages)
        self._caplog.clear()

    def expect_regex(self, *expected_patterns):
        actual_messages = self._pop_messages()
        for pattern in expected_patterns:
            assert any(re.fullmatch(pattern, message) for message in actual_messages)

    def _pop_messages(self):
        messages = [record.getMessage() for record in self._caplog.records]
        self._caplog.clear()
        return messages


@pytest.fixture(scope="function")
def log_checker(caplog):
    caplog.set_level(logging.INFO)
    return LogChecker(caplog)


@pytest.mark.allows_parallel
def test_logging_details(builder, log_checker, parallel_execution_enabled):
    """
    Test the details of the log messages we emit. Since these messages are currently the
    best way to get visibility into what Bionic is doing, we have much more detailed
    tests than we'd normally want for logging. This means we'll have to tweak these
    tests as we update the format or implementation details of our logging.

    At some point we should introduce a separate system for user-facing
    progress reporting instead of using logs.
    """

    builder.assign("x", 1)

    @builder
    def x_plus_one(x):
        return x + 1

    @builder
    def x_plus_two(x_plus_one):
        return x_plus_one + 1

    flow = builder.build()
    assert flow.get("x_plus_one") == 2
    log_checker.expect_all(
        "Accessed   x(x=1) from definition",
        "Computing  x_plus_one(x=1) ...",
        "Computed   x_plus_one(x=1)",
    )

    assert flow.get("x_plus_two") == 3

    if parallel_execution_enabled:
        # This is different from serial execution because we don't pass
        # in-memory cache to the subprocesses. The subprocess loads the
        # entities from disk cache instead.
        log_checker.expect_all(
            "Loaded     x_plus_one(x=1) from disk cache",
            "Computing  x_plus_two(x=1) ...",
            "Computed   x_plus_two(x=1)",
        )
    else:
        log_checker.expect_all(
            "Accessed   x_plus_one(x=1) from in-memory cache",
            "Computing  x_plus_two(x=1) ...",
            "Computed   x_plus_two(x=1)",
        )

    flow = builder.build()
    assert flow.get("x_plus_one") == 2
    # We don't access the definitions for simple lookup objects in
    # parallel execution unless we use the objects for computation.
    # Since we load x_plus_one from disk cache, we don't access the
    # definition for x.
    # To clarify: we do access it for looking at the cache, but it's
    # taken from the case key where it is loaded by default and is not
    # counted as definition access in the flow.
    log_checker.expect_all("Loaded     x_plus_one(x=1) from disk cache")

    flow = builder.build()
    assert flow.get("x_plus_two") == 3
    log_checker.expect_all("Loaded     x_plus_two(x=1) from disk cache")

    flow = flow.setting("x_plus_one", 3)
    assert flow.get("x_plus_two") == 4
    log_checker.expect_all(
        "Accessed   x_plus_one(x_plus_one=3) from definition",
        "Computing  x_plus_two(x_plus_one=3) ...",
        "Computed   x_plus_two(x_plus_one=3)",
    )


class CannotPickleMe:
    def __init__(self):
        # Storing a lock makes it unpickleable
        self.lock = threading.Lock()

    def __str__(self):
        return "Cannot pickle me"


def test_log_unpickleable_value(builder, log_checker):
    @builder
    def log_unpickleable_value():
        # Test that we handle unpickleable value in `LogRecord.msg`.
        logging.info(CannotPickleMe())
        # Test that we handle unpickleable value in `LogRecord.args`.
        logging.info("Logging unpickleable class: %s", CannotPickleMe())
        return 5

    assert builder.build().get("log_unpickleable_value") == 5

    log_checker.expect_all(
        "Computing  log_unpickleable_value() ...",
        "Cannot pickle me",
        "Logging unpickleable class: Cannot pickle me",
        "Computed   log_unpickleable_value()",
    )


@pytest.mark.no_parallel
@pytest.mark.needs_aip
def test_log_aip(aip_builder, log_checker):
    builder = aip_builder

    builder.assign("x", 1)

    @builder
    @bn.aip_task_config("n1-standard-4")
    def x_plus_one(x):
        return x + 1

    @builder
    @bn.aip_task_config("n1-standard-8")
    def x_plus_two(x_plus_one):
        return x_plus_one + 1

    flow = builder.build()

    assert flow.get("x_plus_one") == 2

    log_checker.expect_regex(
        r"Accessed   x\(x=1\) from definition",
        r"Uploading x\(x=1\) to GCS ...",
        r"Staging task .* at gs://.*",
        r"Submitting .*x_plus_one.*",
        r"Started task on AI Platform: https://console.cloud.google.com/ai-platform/jobs/.*",
        r"Computed   x_plus_one\(x=1\) using AIP",
    )

    assert flow.get("x_plus_two") == 3

    # Unfortunately, the string "Loaded     x_plus_one(x=1) from disk cache" is
    # printed in AIP logs but not locally.

    log_checker.expect_regex(
        r"Staging task .* at gs://.*",
        r"Submitting .*x_plus_two.*",
        r"Started task on AI Platform: https://console.cloud.google.com/ai-platform/jobs/.*",
        r"Computed   x_plus_two\(x=1\) using AIP",
    )
