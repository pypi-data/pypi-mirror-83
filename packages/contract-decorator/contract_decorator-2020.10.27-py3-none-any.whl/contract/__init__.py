"""
   Copyright 2020 Claudio Corsi

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

"""

__all__ = ["contract", "validvalues", "checktype", "closed", "opened", "closedopened", "openedclosed", "gt", "lt",
           "gteq", "lteq"]

__version__ = '2020.10.20'
__author__ = 'Claudio Corsi'

"""
NOTE: This code was inspired by the following sources:

  - https://wiki.python.org/moin/PythonDecoratorLibrary#Pre-.2FPost-Conditions
  - https://github.com/andrewp-as-is/accepts.py/blob/master/accepts/__init__.py

Objective:

To be able to allow for a wide range of parameter checking that can be used by
anyone without having to include the parameter checks within the calling method.
This will allow someone to provide cleaner code for the implemented method while
adding some complexity to the decorator.

"""
import inspect


# Checks that the value is an instance of type t
class CheckType(object):
    def __init__(self, t):
        self._t = t

    def __call__(self, v):
        assert isinstance(v, self._t), "Invalid type expected: {}, was: {}".format(self._t, type(v))


# [a,b]
class CheckClosedRange(object):
    def __init__(self, a, b):
        self._a = a
        self._b = b

    def __call__(self, v):
        assert self._a <= v, 'Incorrect value {} has to be greater than or equal to {}'.format(v, self._a)
        assert self._b >= v, 'Incorrect value {} has to be less than or equal to {}'.format(v, self._b)


# (a,b)
class CheckOpenedRange(object):
    def __init__(self, a, b):
        self._a = a
        self._b = b

    def __call__(self, v):
        assert self._a < v, 'Incorrect value {} has to be greater than {}'.format(v, self._a)
        assert self._b > v, 'Incorrect value {} has to be less than {}'.format(v, self._b)


# (a,b]
class CheckOpenedClosedRange(object):
    def __init__(self, a, b):
        self._a = a
        self._b = b

    def __call__(self, v):
        assert self._a < v, 'Incorrect value {} has to be greater than {}'.format(v, self._a)
        assert self._b >= v, 'Incorrect value {} has to be less than or equal to {}'.format(v, self._b)


# [a.b)
class CheckClosedOpenedRange(object):
    def __init__(self, a, b):
        self._a = a
        self._b = b

    def __call__(self, v):
        assert self._a <= v, 'Incorrect value {} has to be greater than {}'.format(v, self._a)
        assert self._b > v, 'Incorrect value {} has to be less than {}'.format(v, self._b)


# < a
class LessThan(object):
    def __init__(self, a):
        self._a = a

    def __call__(self, v):
        assert v < self._a, 'Invalid value {} should be less than {}'.format(v, self._a)


# > a
class GreaterThan(object):
    def __init__(self, a):
        self._a = a

    def __call__(self, v):
        assert v > self._a, 'Invalid value {} should be greater than {}'.format(v, self._a)


# <= a
class LessThanOrEqual(object):
    def __init__(self, a):
        self._a = a

    def __call__(self, v):
        assert v <= self._a, 'Invalid value {} should be less than or equal {}'.format(v, self._a)


# >= a
class GreaterThanOrEqual(object):
    def __init__(self, a):
        self._a = a

    def __call__(self, v):
        assert v >= self._a, 'Invalid value {} should be greater than or equal {}'.format(v, self._a)


# Checks that the value passed is contained within the expected values.
# The passed expected value has to be a tuple such that the 'in' command
# is defined as the passed expected value tuple.
class ValidateValues(object):
    def __init__(self, values):
        self._values = values

    def __call__(self, v):
        assert v in self._values, 'Invalid value {} should be one of {}'.format(v, self._values)


def validvalues(values):
    return ValidateValues(values)


def checktype(t):
    return CheckType(t)


def closed(a, b):
    return CheckClosedRange(a, b)


def opened(a, b):
    return CheckOpenedRange(a, b)


def closedopened(a, b):
    return CheckClosedOpenedRange(a, b)


def openedclosed(a, b):
    return CheckOpenedClosedRange(a, b)


def gt(a):
    return GreaterThan(a)


def lt(a):
    return LessThan(a)


def gteq(a):
    return GreaterThanOrEqual(a)


def lteq(a):
    return LessThanOrEqual(a)


def _assigngetargsspec():
    """
    This method will determine which method should be used to extract the method information.
    The reason behind this call is that the getfullargspec method was not introduced within
    the initial release of python 3.0.  Thus, we are determining which method should be used.
    We are then boxing in this check within this code which will make the code calling this
    cleaner.

    :return:  The method that can be used to extract parameter information for a given
        method.
    """
    if (hasattr(inspect, 'getfullargspec')):
        return inspect.getfullargspec
    else:
        return inspect.getargspec


getargsspec = _assigngetargsspec()

"""
To be implemented.
These are just more efficient implementation of the general
checks decorator.

def checktypes(f,checks=()):
  pass

def checkvalues(f,checks=()):
  pass
"""


class CheckFunction(object):
    def __init__(self, func, checks):
        self._func = func
        self._checks = checks
        self._signs = {}
        try:
            sig = inspect.signature(func)
            for idx, name in enumerate(sig.parameters):
                self._signs[name] = idx
        except Exception as ex:
            # TBD: Should we be raising this exception or just leave it alone?
            print('an exception was raised when getting the function signature', ex)

    def __call__(self, *args, **kwargs):
        # Figure out how to determine what parameters have
        # been passed and then apply the different checks
        # for each of the passed parameters until the checks
        # have been exhausted or an invalid condition has been
        # encountered.
        global getargsspec
        # Get the current method arguments specification
        fargsspec = getargsspec(self._func)
        # Process each parameter value and apply the checks
        # to each parameter that has one or more defined.
        for idx, value in enumerate(args):
            # Determine if the current parameter has an associated contract check that needs to be applied.
            if (fargsspec.args[idx] in self._checks):
                # Check that the passed set of checks are contained within a iterable type object
                # by looking for the __iter__ method.
                assert hasattr(self._checks[fargsspec.args[idx]], "__iter__"), \
                    "Invalid type {}, it should be a tuple type for parameter: {}".format(
                        type(self._checks[fargsspec.args[idx]]), fargsspec.args[idx])
                # Iterate through each contract check and call it passing the current parameter value
                for check in self._checks[fargsspec.args[idx]]:
                    check(value)
        # Process each of the passed dictionary name/value pairs
        for name, value in kwargs.items():
            if (name in self._checks):
                for check in self._checks[name]:
                    check(value)

        # Call the method and forward the parameter values while storing the
        # return value that can then be checked prior to returning from the
        # called method.
        returnValue = self._func(*args, **kwargs)

        # Determine if the returned value abides to the required
        # contract.
        if (None in self._checks):
            self._checks(returnValue)

        return returnValue


class contract(object):
    """
  Contract Decorator:
    This decorator can be used to associate method specific conditions that have to been maintained during
    runtime.  This will allow the developer to move the parameter contract to be checked outside of the
    calling method.  This provides for a cleaner method without the added parameter checking.  This
    decorator also provides the ability to check the returning valuing.  Thus not limiting this check
    to only the passing parameter values.
  """

    def __init__(self, conditions):
        # Check that the passed checks is a dictionary
        assert isinstance(conditions, dict), "Invalid type {} for parameter checks, supposed to be a dict".format(
            type(conditions))
        # Check that each value is an iterable tuple
        for key, value in conditions.items():
            assert hasattr(value, "__iter__"), "Invalid type {} for key {}, supposed to be an iterable instance".format(
                type(value), key)
            for check in value:
                # Determine if we are passed a class instance
                if inspect.isclass(type(check)):
                    # Insure that the class instance has a callable method
                    assert hasattr(check,
                                   "__call__"), "Invalid type {}, supposed to be a callable instance".format(type(check))

        self._checks = conditions

    def __call__(self, f):
        # Initialize the instance that will perform the checks
        def check(*args, **kwargs):
            conditions = CheckFunction(f, self._checks)
            return conditions(*args, **kwargs)

        return check
