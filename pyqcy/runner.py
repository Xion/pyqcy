"""
Simple, built-in test runner.
"""
import sys
import traceback

from pyqcy.properties import Property
from pyqcy.utils import partition


__all__ = ['main']


def main(module='__main__', exit=True, verbosity=2, failfast=False):
    """Built-in test runner for properties.

    When called, it will look for all properties (i.e. functions with
    :func:`qc` decorator) and run checks on them.

    Arguments are intended to mimic those from :func:`unittest.main`.
    Return value is the total number of properties checked,
    provided ``exit`` is ``False`` and program doesn't terminate.
    """
    if isinstance(module, basestring):
        module_name = module
        module = __import__(module_name)
        for part in module_name.split('.')[1:]:
            module = getattr(module, part)

    props = [v for v in module.__dict__.itervalues()
             if isinstance(v, Property)]

    success = run_tests(props, verbosity=verbosity, failfast=failfast)
    if exit:
        sys.exit(0 if success else 1)
    return len(props)


def run_tests(props, verbosity=1, failfast=False, propagate_exc=False):
    """Executes tests for given list of properties.
    Returns boolean flag indicating if all the tests succeeded.
    """
    verbosity = verbosity or 0
    success = True

    for p in props:
        results = p.check()
        failed = [r for r in results if not r.succeeded]
        if failed:
            failure = failed[0]

            if verbosity >= 1:
                success_count = p.tests_count - len(failed)
                print "%s: failed (only %s out of %s tests passed)." % (
                    p.func.__name__, success_count, p.tests_count)
                print "Failure encountered for data:"
                for k, arg in failure.data.iteritems():
                    print "  %s = %s" % (k, repr(arg))

                print "Exception:"
                traceback.print_exception(type(failure.exception),
                                          failure.exception, failure.traceback)

            success = False
            if failfast:
                break
            if propagate_exc:
                failure.propagate_failure()
        else:
            if verbosity >= 2:
                tags = (r.tags for r in results)
                print_test_results(p, tags)

    return success


def print_test_results(prop, results):
    """Prints results of testing a single property.

    Results include any statistical information that the property
    has generated though ``yield`` statements.
    """
    print "%s: passed %s test%s." % (prop.func.__name__,
                                     prop.tests_count,
                                     "s" if prop.tests_count != 1 else "")

    # gather and display statistics
    results = list(results)
    with_stats, without_stats = partition(lambda r: len(r) > 0, results)
    if len(with_stats) > 0:
        stats = {}
        for s in with_stats:
            stats[s] = stats.get(s, 0) + 1
        stats = stats.items()
        if len(without_stats) > 0:
            stats.append(("<rest>", len(without_stats)))

        results_count = float(len(results))
        for labels, count in stats:
            percentage = "%.2f%%" % (count * 100 / results_count)
            summary = ", ".join(map(str, labels))
            print "%s: %s" % (percentage.rjust(5), summary)
