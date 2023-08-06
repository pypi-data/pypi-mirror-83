# -*- coding: UTF-8 -*-
#
# SPDX-License-Identifier: MIT
# Copyright (c) 2011-2017, 2019 Felix Schwarz <felix.schwarz@oss.schwarz.eu>
# Copyright (c)      2012 Robert Buchholz <rbu@goodpoint.de>

# TODO / nice to have
#  - raising assertions (with message building) should be unified
#  - shorted tracebacks for cascaded calls so it's easier to look at the
#    traceback as a user
#      see jinja2/debug.py for some code that does such hacks:
#          https://github.com/mitsuhiko/jinja2/blob/master/jinja2/debug.py

from __future__ import absolute_import, unicode_literals, print_function

from contextlib import contextmanager
from datetime import datetime as DateTime, timedelta as TimeDelta, tzinfo as TZInfo
import functools
import os
from unittest import TestCase
import sys

try:
    # Python 3.2+
    from datetime import timezone as TimeZone
    UTC = TimeZone.utc
except ImportError:
    UTC = None


__all__ = ['assert_almost_equals', 'assert_callable', 'assert_contains',
           'assert_dict_contains', 'assert_equals', 'assert_false', 'assert_falseish',
           'assert_file_exists',
           'assert_file_not_exists',
           'assert_greater',
           'assert_is',
           'assert_is_not',
           'assert_isinstance', 'assert_is_empty', 'assert_is_not_empty',
           'assert_length', 'assert_none',
           'assert_not_raises',
           'assert_not_contains', 'assert_not_none', 'assert_not_equals',
           'assert_almost_now',
           'assert_path_exists',
           'assert_path_not_exists',
           'assert_raises', 'assert_smaller', 'assert_true', 'assert_trueish',
           'create_spy', 'expect_failure', 'PythonicTestCase',
           'skip_test', 'skipTest', 'SkipTest',
]

# This simple line instructs some test runners (e.g. stock unittest, nosetests,
# nose2) to suppress all lines referring to code within this module.
# This is helpful because users are usually not interested in the internal
# implementation of PythonicTestcase. Instead they'll see their assertion code
# more prominently.
# Set this line to False if you develop/debug the actual PythonicTestcase code.
__unittest = True

class NotSet(object):
    pass

class _AssertionState(object):
    def __init__(self):
        self.caught_exception = None

@contextmanager
def _assert_raises_context(exception, message):
    context = _AssertionState()
    try:
        yield context
    except exception as e:
        context.caught_exception = e
    else:
        default_message = '%s not raised!' % exception.__name__
        if message is None:
            raise AssertionError(default_message)
        raise AssertionError(default_message + ' ' + message)

def assert_raises(exception, callable=NotSet, message=None):
    context = _assert_raises_context(exception, message=message)
    if callable is NotSet:
        return context
    with context as c:
        callable()
    return c.caught_exception


@contextmanager
def _assert_not_raises_context(exception, message):
    context = _AssertionState()
    try:
        yield context
    except exception as e:
        default_message = 'unexpected exception %r' % e
        if message is None:
            raise AssertionError(default_message)
        raise AssertionError(default_message + ': ' + message)

def assert_not_raises(exception=Exception, callable=NotSet, message=None):
    context = _assert_not_raises_context(exception, message=message)
    if callable is NotSet:
        return context
    with context:
        callable()


def assert_equals(expected, actual, message=None):
    if expected == actual:
        return
    default_message = '%s != %s' % (repr(expected), repr(actual))
    if message is None:
        raise AssertionError(default_message)
    raise AssertionError(default_message + ': ' + message)

def assert_is(expr1, expr2, message=None):
    if expr1 is expr2:
        return
    default_message = '%s is not %s' % (repr(expr1), repr(expr2))
    if message is None:
        raise AssertionError(default_message)
    raise AssertionError(default_message + ': ' + message)

def assert_is_not(expr1, expr2, message=None):
    if expr1 is not expr2:
        return
    default_message = '%s is identical to %s' % (repr(expr1), repr(expr2))
    if message is None:
        raise AssertionError(default_message)
    raise AssertionError(default_message + ': ' + message)

def assert_none(actual, message=None):
    assert_equals(None, actual, message=message)

def assert_false(actual, message=None):
    assert_equals(False, actual, message=message)

def assert_falseish(actual, message=None):
    if not actual:
        return
    default_message = '%s is not falseish' % repr(actual)
    if message is None:
        raise AssertionError(default_message)
    raise AssertionError(default_message + ': ' + message)

def assert_true(actual, message=None):
    assert_equals(True, actual, message=message)

def assert_trueish(actual, message=None):
    if actual:
        return
    default_message = '%s is not trueish' % repr(actual)
    if message is None:
        raise AssertionError(default_message)
    raise AssertionError(default_message + ': ' + message)

def assert_length(expected_length, actual_iterable, message=None):
    length_iterable = _get_length(actual_iterable)
    assert_equals(expected_length, length_iterable, message=message)

def _get_length(actual_iterable):
    try:
        nr_items = len(actual_iterable)
    except TypeError:
        nr_items = len(tuple(actual_iterable))
    return nr_items

def assert_not_equals(expected, actual, message=None):
    if expected != actual:
        return
    default_message = '%s == %s' % (repr(expected), repr(actual))
    if message is None:
        raise AssertionError(default_message)
    raise AssertionError(default_message + ': ' + message)

def assert_almost_equals(expected, actual, max_delta=None, message=None):
    if expected == actual:
        return
    if (max_delta is not None) and (abs(expected - actual) <= max_delta):
        return

    if max_delta is None:
        default_message = '%s != %s' % (repr(expected), repr(actual))
    else:
        default_message = '%s != %s +/- %s' % (repr(expected), repr(actual), repr(max_delta))
    if message is None:
        raise AssertionError(default_message)
    raise AssertionError(default_message + ': ' + message)

def assert_not_none(actual, message=None):
    assert_not_equals(None, actual, message=message)

def assert_contains(expected_value, actual_iterable, message=None):
    if expected_value in actual_iterable:
        return
    default_message = '%s not in %s' % (repr(expected_value), repr(actual_iterable))
    if message is None:
        raise AssertionError(default_message)
    raise AssertionError(default_message + ': ' + message)

def assert_not_contains(expected_value, actual_iterable, message=None):
    if expected_value not in actual_iterable:
        return
    default_message = '%s in %s' % (repr(expected_value), repr(actual_iterable))
    if message is None:
        raise AssertionError(default_message)
    raise AssertionError(default_message + ': ' + message)

def assert_dict_contains(expected_sub_dict, actual_super_dict, message=None):
    for key, value in expected_sub_dict.items():
        assert_contains(key, actual_super_dict, message=message)
        if value != actual_super_dict[key]:
            failure_message = '%(key)s=%(expected)s != %(key)s=%(actual)s' % \
                dict(key=repr(key), expected=repr(value), actual=repr(actual_super_dict[key]))
            if message is not None:
                failure_message += ': ' + message
            raise AssertionError(failure_message)

def assert_is_empty(actual, message=None):
    len_actual = _get_length(actual)
    if len_actual == 0:
        return
    default_message = '%r is not empty (%d items)' % (actual, len_actual)
    default_message = '%r is not empty' % (actual)
    if message is None:
        raise AssertionError(default_message)
    raise AssertionError(default_message + ': ' + message)

def assert_is_not_empty(actual, message=None):
    if _get_length(actual) > 0:
        return
    default_message = '%s is empty' % (repr(actual))
    if message is None:
        raise AssertionError(default_message)
    raise AssertionError(default_message + ': ' + message)

def assert_callable(value, message=None):
    if callable(value):
        return
    default_message = "%s is not callable" % repr(value)
    if message is None:
        raise AssertionError(default_message)
    raise AssertionError(default_message + ': ' + message)

def assert_isinstance(value, klass, message=None):
    if isinstance(value, klass):
        return

    def class_name(instance_or_klass):
        if isinstance(instance_or_klass, type):
            return instance_or_klass.__name__
        return instance_or_klass.__class__.__name__
    default_message = "%s (%s) is not an instance of %s" % (repr(value), class_name(value), class_name(klass))
    if message is None:
        raise AssertionError(default_message)
    raise AssertionError(default_message + ': ' + message)

def assert_smaller(smaller, greater, message=None):
    if smaller < greater:
        return
    default_message = '%s >= %s' % (repr(smaller), repr(greater))
    if message is None:
        raise AssertionError(default_message)
    raise AssertionError(default_message + ': ' + message)

def assert_greater(greater, smaller, message=None):
    if greater > smaller:
        return
    default_message = '%s <= %s' % (repr(greater), repr(smaller))
    if message is None:
        raise AssertionError(default_message)
    raise AssertionError(default_message + ': ' + message)

def assert_path_exists(path, message=None):
    if os.path.exists(path):
        return
    default_message = "path '%s' does not exist" % (path,)
    if message is None:
        raise AssertionError(default_message)
    raise AssertionError(default_message + ': ' + message)

def assert_path_not_exists(path, message=None):
    if not os.path.exists(path):
        return
    default_message = "path '%s' exists" % (path,)
    if message is None:
        raise AssertionError(default_message)
    raise AssertionError(default_message + ': ' + message)

def assert_file_exists(path, message=None):
    if os.path.isfile(path):
        return
    if os.path.exists(path) and os.path.isdir(path):
        default_message = "'%s' is a directory" % (path,)
    else:
        default_message = "file '%s' does not exist" % (path,)
    if message is None:
        raise AssertionError(default_message)
    raise AssertionError(default_message + ': ' + message)

def assert_file_not_exists(path, message=None):
    if not os.path.isfile(path):
        return
    default_message = "file '%s' exists" % (path,)
    if message is None:
        raise AssertionError(default_message)
    raise AssertionError(default_message + ': ' + message)

def assert_almost_now(datetime, max_delta=None, tz=None, message=None):
    if max_delta is None:
        max_delta = TimeDelta(seconds=1)
    elif not isinstance(max_delta, TimeDelta):
        max_delta = TimeDelta(seconds=max_delta)
    has_tz = datetime.tzinfo
    if tz is None:
        tz = UTC if has_tz else None
    elif not has_tz:
        raise AssertionError('%r is not timezone-aware but tz=%r was passed to assert_almost_equals()' % (datetime, tz))

    now = DateTime.now(tz=tz)
    if datetime >= now - max_delta:
        return
    default_message = '%r is older than %s seconds' % (datetime, _total_seconds(max_delta))
    if message is None:
        raise AssertionError(default_message)
    raise AssertionError(default_message + ': ' + message)

def _total_seconds(timedelta):
    if hasattr(timedelta, 'total_seconds'):
        # Python 3.2+
        return timedelta.total_seconds()
    return (timedelta.days * 24 * 60 * 60) + timedelta.seconds + (timedelta.microseconds / 1000000)


def create_spy(name=None):
    class Spy(object):
        def __init__(self, name=None):
            self.name = name
            self.reset()

        # pretend to be a python method / function
        @property
        def func_name(self):
            return self.name

        def __str__(self):
            if self.was_called:
                return "<Spy(%s) was called with args: %s kwargs: %s>" \
                    % (self.name, self.args, self.kwargs)
            else:
                return "<Spy(%s) was not called yet>" % self.name

        def reset(self):
            self.args = None
            self.kwargs = None
            self.was_called = False
            self.return_value = None

        def __call__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs
            self.was_called = True
            return self.return_value

        def and_return(self, value):
            self.return_value = value
            return self

        def assert_was_called_with(self, *args, **kwargs):
            assert_true(self.was_called, message=str(self))
            assert_equals(args, self.args, message=str(self))
            assert_equals(kwargs, self.kwargs, message=str(self))

        def assert_was_called(self):
            assert_true(self.was_called, message=str(self))

        def assert_was_not_called(self):
            assert_false(self.was_called, message=str(self))

    return Spy(name=name)

# --- SkipTest support -------------------------------------------------------
# unfortunately SkipTest was only added in the unittest module for Python 2.7.
# However nosetests supports this even on Python 2.6. And while we're at it,
# let's also not forget about unittest2
try:
    from unittest.case import SkipTest
except ImportError:
    try:
        from unittest2.case import SkipTest
    except ImportError:
        try:
            from nose import SkipTest
        except ImportError:
            # Python 2.6 without unittest2 or nosetests - we can't win here
            # but at least let's not break as long as the user won't try to
            # use the SkipTest functionality
            SkipTest = AssertionError
def skip_test(*args, **kwargs):
    raise SkipTest(*args, **kwargs)
# ensure that nosetests does not try to run this function as "test"
skip_test.__test__ = False
skipTest = skip_test

# --- expect_failure support --------------------------------------------------
# unittest in Python 2.7 introduced the "expectedFailure" decorator. We should
# provide support for Python 2.6 and I'd like to report failing "expected
# failures" as "skipped", not "passing".

IS_PYTHON3 = (sys.version_info >= (3, 0))
IS_PYTHON34_OR_LATER = (sys.version_info >= (3, 4))
try:
    from unittest.case import _ExpectedFailure
except ImportError:
    _ExpectedFailure = SkipTest

def expect_failure(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            f(*args, **kwargs)
        except AssertionError:
            if IS_PYTHON34_OR_LATER:
                raise
            raise _ExpectedFailure(sys.exc_info())
        raise AssertionError('expected failure but test seems to pass just fine')
    if IS_PYTHON34_OR_LATER:
        wrapper.__unittest_expecting_failure__ = True
    return wrapper

def add_expected_failure_py(result, test, err):
    result.addSkip(test, str(err))

# --- other helpers -----------------------------------------------------------
class _UTC(TZInfo):
    def utcoffset(self, dt):
        return TimeDelta(seconds=0)

    def dst(self, dt):
        return TimeDelta(seconds=0)

    def __repr__(self):
        return '<UTC>'


if UTC is None:
    UTC = _UTC()

# --- unittest.TestCase alternative with pythonic names -----------------------
from types import MethodType

class PythonicTestCase(TestCase):
    def __getattr__(self, name):
        globals_ = globals()
        if name in globals_:
            return globals_[name]
        return getattr(super(PythonicTestCase, self), name)

    def run(self, result=None):
        if (result is not None) and (not hasattr(result, 'addExpectedFailure')):
            if IS_PYTHON3:
                result.addExpectedFailure = MethodType(add_expected_failure_py, result)
            else:
                result.addExpectedFailure = MethodType(add_expected_failure_py, result, result.__class__)
        return super(PythonicTestCase, self).run(result=result)


# is_callable

