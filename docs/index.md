# NewerType

An Implementation of the NewType Pattern for Python that works in dynamic contexts.

!!! warning "Breaking Change coming in 1.0"
    **Version 1.0 will introduce type caching**, which changes behavior from previous versions:

    - Calling `NewerType` with the same parameters will return the **same type object** (cached)
    - Currently, each call created a **new type object**

    This code is already in 0.4.0, but inactive.

    To start using it now:

    ```python
    Type = NewerType("SomeType", int, use_cache=True)
    ```

    **Migration:** If your code depends on getting different types from duplicate calls, use `use_cache=False`:

    ```python
    # Current behavior (each call creates a new type)
    Type1 = NewerType("MyType", int, use_cache=False)
    Type2 = NewerType("MyType", int, use_cache=False)
    assert Type1 is not Type2  # Different types
    ```

    For most users, the new caching behavior will be more intuitive and will improve performance.

## What is it?

`NewerType` is a package that provides a semi-transparent wrapper to an existing type that allows it to be used mostly as if it's just the wrapped type, but which allows type checking as if it's a distinct type at runtime.

With the addition to Python of [PEP 483](https://peps.python.org/pep-0483/), [PEP 484](https://peps.python.org/pep-0484/), & the [typing](https://docs.python.org/3/library/typing.html#module-typing) package, Python added support for type hints. That included an implementation of the Haskell [`newtype`](https://wiki.haskell.org/Newtype) which was cleverly called `NewType`.

As explained in [the documentation](https://docs.python.org/3/library/typing.html#typing.NewType), Python's `NewType` is, like most of the typing library, meant for use by static type checkers. This means that, when the code is running, the _Newness_ of the type is erased, leaving just the wrapped type & no way to tell that there was ever a `Newtype`, either by the code or by Python itself.

`NewerType` provides the same kind of wrapper as `NewType`, but allows (& enforces) type checking at runtime. This means, for example, that if you wrap an `int` in a `NewerType`, you can do all of the arithmetic & comparison operations on an instance of that type that you could with a normal `int` with either different instances of that type, or `int`s. But you will not be able to mix _different_ `NewerType`s, even if they all wrap `int`s.

This allows you to never have to worry if you are adding `Miles` to `Kilometers`, or mixing up a `UserName` with a `Password`.

## Main Features

* A wrapper that allows dynamic type checking while mostly not getting in the way
* Carries type information with the object so you can always use `isinstance()` or `type()` to know what it is
* Forwards the magic methods from the wrapped object so things like arithmetic or indexing work
* Allows you to customize what methods are forwarded
* No dependencies!

## Installation

### Using pip

Install the latest stable version:
```shell
pip install newertype
```

### From source

```shell
pip install git+https://github.com/evanjpw/newertype.git
```

## Requirements

- Python 3.8 or higher
- No external dependencies!

## Quick Start

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
AType = NewerType("AType", int)
a_type_1 = AType(7)
a_type_2 = AType(7)
a_type_1 == a_type_2  # You can compare them as if they were just `int`s
# Returns: True

EType = NewerType("EType", int)
e_type_1 = EType(7)
e_type_2 = EType(14)
e_type_2 > e_type_1  # All of the `int` operations work
# Returns: True
a_type_1 == e_type_1  # But different types are not equal, even if the wrapped value is
# Returns: False

IType = NewerType("IType", int)
i_type_1 = IType(7)
i_type_2 = IType(14)
i_type_1 + i_type_2  # Arithmetic works!
# Returns: 21

JType = NewerType("JType", int)
j_type_1 = JType(7)
i_type_1 + j_type_1  # But not if you try to mix `NewerType`s
# TypeError: unsupported operand type(s) for +: 'IType' and 'JType'
```

## Next Steps

- Check out the [API Reference](api.md) for detailed documentation
- See the [Changelog](https://github.com/evanjpw/newertype/blob/main/CHANGELOG.md) for version history
