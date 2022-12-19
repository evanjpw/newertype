# newertype

An Implementation of the NewType Pattern for Python that works in dynamic contexts.

## What is it?

`NewerType` is a package that provides a semi-transparent wrapper to an existing type that allows it to be used
mostly as if it's just the wrapped type, but which allows type checking as if it's a distinct type at runtime.

With the addition to Python of [PEP 483](), [PEP 484](), & the [typing]() package, Python added support for type
hints. That included an implementation of the Haskell [`newtype`](https://wiki.haskell.org/Newtype) which was
cleverly called `NewType`. As explained in [the documentation](), Python's `NewType` is, like most of the
typing library, meant for use by static type checkers. This means that, when the code is running, the _Newness_ of
the type is erased, leaving just the wrapped type & no way to tell that there was ever a `Newtype`, either by
the code or by Python itself.

`NewerType` provides the same kind of wrapper as `NewType`, but allows (& enforces) type checking at runtime.
this means, for example, that if you wrap an `int` in a `NewerType`, you can do all of the arithmetic &
comparison operations on an instance of that type that you could with a normal `int` with either different
instances of that type, or `int`s. But you will not be able to mix _different_ `NewerType`s, even if they
all wrap `int`s.

This allows you to never have to worry if you are adding `Miles` to `Kilometers`, or mixing up a `UserName`
with a `Password`.

### Main Features

* 

## Installation

Current stable version (**not yet!**):
```shell
pip install newertype
```

Newest thing on GitHub:
```shell
pip install git+https://github.com/evanjpw/newertype.git
```

## Usage

Basic usage:

```python
from newertype import NewerType

AType = NewerType("AType", int)  # `AType` is a new type that wraps an int
a_type = AType(14)  # Make an instance of this new type
isinstance(a_type, AType)  # `a_type` is an `AType`
# Returns: True
isinstance(a_type, int)  # `a_type` is _NOT_ an `int`
# Returns: False
str(a_type.__class__.__name__) == "AType"
# Returns: True
```

You can use the new type as if it's the wrapped type:

```python
AType = NewerType("AType", int)  # Let's make some types!
a_type_1 = AType(7)
a_type_2 = AType(7)  # Two different instances with the same class
a_type_1 == a_type_2  # You can compare them as if they were just `int`s
# Returns: True

EType = NewerType("EType", int)
e_type_1 = EType(7)
e_type_2 = EType(14)
e_type_2 > e_type_1  # All of the `int` operations work
# Returns: True
a_type_1 != e_type_1  # But different types are not equal, even if the wrapped value is
Returns: False

IType = NewerType("IType", int)
JType = NewerType("JType", int)
i_type_1 = IType(7)
i_type_2 = IType(14)
i_type_1 + i_type_2  # Arithmetic works!
# Returns: 21

j_type_1 = JType(7)
i_type_1 + j_type_1  # But not if you try to mix `NewerType`s
# "TypeError: unsupported operand type(s) for +: 'IType' and 'JType'"
int(i_type_1) < int(i_type_2)  # Conversions that work for the inner type work also
# Returns: True
```

Accessing the wrapped data directly:

```python
a_type = AType(14)
a_type.inner  # the `inner` property gets the contained value
# Returns: 14
a_type.inner = 27  # `inner` can also be used to modify the value
a_type.inner
# Returns: 27
```

The "truthiness" & string representations are sensible:

```python
SType = NewerType("SType", float)
s_type = SType(2.71828182845904523536028747135266249775724709369995)
str(s_type)
# Returns: "SType(2.718281828459045)"
repr(s_type)
# Returns: "SType(2.718281828459045)"
bool(s_type)
# Returns: True
bytes(s_type)  # `bytes only works if it works with the wrapped type
# "TypeError: cannot convert 'float' object to bytes"

s_type.inner = 0.0
bool(s_type)
# Returns: False
```

## TBD

## Project Resources

* Documentation - TBD
* Issue tracker - TBD
* Source code - TBD
* Change log - TBD

## License

Licensed under the [MIT LICENSE](https://www.mit.edu/~amini/LICENSE.md)
