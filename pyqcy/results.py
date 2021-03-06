"""
Code related to results of tests.
"""
import os
import sys


class CheckError(Exception):
    """Exception raised when property test fails.

    It constains the original test data for which
    the test has failed.
    """
    def __init__(self, data, cause=None):
        self.test_data = data
        self.cause = cause

    def __str__(self):
        msg = "test failed"
        if self.cause is not None:
            msg += " due to %s" % type(self.cause).__name__
            cause = str(self.cause)
            if cause:
                msg += ": " + cause

        res = [msg]
        res.append("Failure encountered for data:")
        res.extend(["  %s = %s" % i for i in self.test_data.iteritems()])
        return os.linesep.join(res)


class TestResult(object):
    """An object that holds the results of single test run
    for particular property.

    Results include the original test data,
    all the tags generated by property,
    and the exception that failed the test, if any.
    """
    def __init__(self, data):
        self.data = data
        self.tags = []

    @property
    def succeeded(self):
        return getattr(self, 'exception', None) is None

    def register_failure(self):
        """Saves the current exception info as a reason for test failure,
        so that it can be subsequently inspected or propagated further.
        """
        _, self.exception, self.traceback = sys.exc_info()

    def propagate_failure(self):
        """Re-raises the exception which caused the property test to fail.

        The exception is raised "seemlessly", i.e. with original traceback,
        like it was never really captured to begin with.
        """
        # This form of 'raise' ensures the original traceback is preserved
        exception = CheckError(data=self.data, cause=self.exception)
        raise type(exception), exception, self.traceback
