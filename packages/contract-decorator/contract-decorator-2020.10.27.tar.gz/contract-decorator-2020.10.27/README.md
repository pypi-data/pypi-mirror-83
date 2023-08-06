# Introduction

The following decorator can be used to provide parameter checking for regular and class methods.  

This decorator would not be possible without the inspiration of the following:

* [So you want to be a Python expert? by James Powell](https://www.youtube.com/watch?v=cKPlPJyQrt4)
* [Pre/Post-Condition Decorator Example](https://wiki.python.org/moin/PythonDecoratorLibrary#Pre-.2FPost-Conditions)
* [Andrew P accepts decorator](https://github.com/andrewp-as-is/accepts.py)

The above inspired me to create this decorator to reduce the clutter of my code.

Even thou the accepts decorator already checks for the type.  It is somewhat limited
because it expects the exact number of parameters of the method.  It forces the users
to decorator all of the parameters instead of the ones that one wants checked.  This 
limitation has been removed for this decorator.

## Objective

To allow for a wide range of parameter checking that can be used by
anyone without having to include the parameter checks within the calling method.
This will allow someone to provide cleaner code for the implemented method while
adding some complexity to the decorator.

## Features

The __contract__ decorator provides the ability for a user to check a parameter for
type and/or value expectation.  This also includes the option of checking the return
value.

The __contract__ decorator uses the following syntax:

```python
    import contract

    @contract({
        'a': [checktype(float), closed(0.0, 1.0)],
        'b': [checktype(int), gteq(1)],
        'c': [checktype(int), gteq(1)]
    })
    def __init__(self,a, b, c, d):

```

The above __contract__ will check that the *a* parameter is of type float and is between 0.0
and 1.0.  While the *b* parameter is checked that is it an integer and is greater than of equal
to 1.  The same for parameter *c*.  While parameter *d* does not required any special condition
to be true.

As can be seen, the __contract__ decorator expects you to pass it a dictionary.  Where the *key*
is the name of the parameter and the *value* is a tuple containing the different checks that will
be called for each parameter value during run-time.

The following table contains the different options that the can be used with this decorator.

| Name | Parameters | Type | Description |
|---|---|---|---|
| validvalues | tuple | Value Check | Checks that the parameter value is part of the tuple |
| checktype | type | Type Check | Checks if the parameter is an instance of the expected type |
| closed | a,b such that a <= b | Closed Range Check | Checks if the value is between two values a and b including a and b |
| opened | a,b such that a < b | Opened Range Check | Checks if the value is between two values a and b excluding a and b |
| closedopened | a,b such that a < b | Closed/Opened Check | Checks if the value is between two values a and b including a but excluding b |
| openedclosed | a,b such that a < b | Opened/Closed Check | Checks if the value is between two values a and b including b but excluding a | 
| gt | a | Value Check | Checks that the parameter value is greater than a | 
| lt | a | Value Check | Checks that the parameter value is less than a |
| gteq | a | Value Check | Checks that the parameter value is greater than or equal to a | 
| lteq | a | Value Check | Checks that the parameter value is less than or equal to a |

## Examples

The following example offers some ways that the __contract__ decorator can be used within someone code.

### Type Check.

The following code shows how you can check that a given parameter is of a given type.

```python
    import contract

    @contract({
        'a': [checktype(float)]
    })
    def m(a):

```

The above will determine if the passed value *a* is a *float* type.

### Range Checks

The following contains the different range checks that can be applied. 

```python
    import contract

    @contract({
        'a': [closed(0, 1)],
        'b': [gteq(2)],
        'c': [gt(3)],
        'd': [lt(4)],
        'e': [lteq(5)],
        'f': [opened(10.0, 11.0)],
        'g': [closedopened(12, 13)],
        'h': [openedclosed(14, 15)],
    })
    def range_check(self,a, b, c, d, e, f, g, h):

```

The above will then perform the expected checks for each of the referenced parameters.

Note that the above checks are not restricted to the primitive values but can be 
any class that implements the different range checks methods of the Data Model. 
You can then use the Range checks with a users defined class that implements 
the \_\_lt\_\_, \_\_le\_\_, \_\_gt\_\_, and \_\_ge\_\_ methods.
  
### Tuple Check

```python
    @contract({
        'a': [validvalues(set('blue','green','red'))]
    })
    def contains(a,b):

```

The above example will insure that the value of parameter *a* will be set to 'blue',
'green' or 'red'.

### Return Value Check

```python
    @contract({
        None: [gt(101)]
    })
    def contains(a,b):

```

The above check will determine that the return value is greater than 100.  Note
that you need to specify that the return parameter name as *None*.  This is how we 
associate the check for the return value.

### User Defined Checks

The contract decorator provides the ability for a user to create their own user defined
checks.  This will allow users to define checks that are not covered above.  There are
two different ways of creating user-defined checks.  You can create a class that has 
a callable defined that expects a single parameter or you can define a method that
expects a single parameter.  Both implementations will be passed the value that was 
passed to the decorated method.  The following section will give examples of each.

#### User Defined Class Check

Here is a simple example of how to create and use a user define class to check
that the passed method parameter value agrees with the method contract.

```python

class UserDefinedCheck(object):
    def __init__(self,cond):
        self.cond_ = cond
        ...

    def __call__(self, v):
        # Example of using a simple assert check
        assert v != None, "The value passed cannot be None"
        # Example of using a simple method or instance object.
        # The method or instance should raise an AssertionError whenever the condition is false
        cond(v) 
        ...

@contract({'a':[UserDefinedCheck()]})
def check_me(a,b):
    ...

```

The *UserDefinedCheck* class that was created above has a distinctive requirement.  
The need for the class to implement the *\_\_call\_\_* method with a single
parameter.  The callable method is called by the contract decorator and it expects
the call to raise an AssertionError whenever the condition is not valid.  Lastly,
the class is used by passing an instance of the *UserDefinedCheck* class to the 
contract decorator.

In the example above, the parameter passed will be the value of the *a* parameter
when the *check\_me* function is called.
  
#### User Defined Method Check

Here is a simple example showing how a user-defined check method can be implemented 
and used by the contract decorator.

```python

def user_defined_check(v):
    assert v != None, 'The value cannot be set to None'
    ...

@contract({'b':[user_defined_check]})
def check_me(a,b):
    ...

```

The *user\_defined\_check* method was created with a similar requirement as the user 
defined class.  The method was defined with a simple parameter.  The contract 
decorator will then pass the value of the checking parameter when the method that
is being checked is called.  Lastly, a reference to the *user\_defined\_check* method
is passed to the contract decorator.

In the example above, the check_me method will use the *user\_defined\_check* method
to check the contract of the *b* parameter. 