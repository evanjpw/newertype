"""Tests for methods added in version 0.3.0."""

import copy
import sys

from newertype import NewerType


def test_ne():
    """Test __ne__ (not equals) forwarding."""
    AType = NewerType("AType", int)
    a1 = AType(5)
    a2 = AType(5)
    a3 = AType(7)
    assert not (a1 != a2)
    assert a1 != a3


def test_hash():
    """Test __hash__ forwarding for hashable types."""
    IType = NewerType("IType", int)
    i1 = IType(42)
    i2 = IType(42)
    # Same value should have same hash
    assert hash(i1) == hash(i2)
    # Can be used in sets/dicts
    type_set = {i1, i2}
    assert len(type_set) == 1


def test_format():
    """Test __format__ forwarding."""
    FType = NewerType("FType", float)
    f = FType(3.14159)
    # Format with 2 decimal places
    assert f"{f:.2f}" == "3.14"
    # Percent format
    assert f"{f:.1%}" == "314.2%"


def test_sizeof():
    """Test __sizeof__ forwarding."""
    IType = NewerType("IType", int)
    i = IType(42)
    # Should return a positive integer
    assert isinstance(sys.getsizeof(i), int)
    assert sys.getsizeof(i) > 0


def test_copy():
    """Test __copy__ forwarding."""
    LType = NewerType("LType", list)
    l1 = LType([1, 2, 3])
    l2 = copy.copy(l1)
    # Should be equal
    assert l1.inner == l2.inner
    # But modifications to inner list should affect both (shallow copy)
    l1.inner.append(4)
    assert l2.inner == [1, 2, 3, 4]


def test_deepcopy():
    """Test __deepcopy__ forwarding."""
    LType = NewerType("LType", list)
    l1 = LType([[1, 2], [3, 4]])
    l2 = copy.deepcopy(l1)
    # Should be equal
    assert l1.inner == l2.inner
    # But modifications to inner list should NOT affect the copy (deep copy)
    l1.inner[0].append(99)
    assert l1.inner == [[1, 2, 99], [3, 4]]
    assert l2.inner == [[1, 2], [3, 4]]


def test_bytes_default_utf8():
    """Test __bytes__ uses UTF-8 by default for strings."""
    SType = NewerType("SType", str)
    s = SType("hello")
    assert bytes(s) == b"hello"

    # Test with non-ASCII characters
    s2 = SType("héllo")
    assert bytes(s2) == "héllo".encode()


def test_bytes_non_string():
    """Test __bytes__ with non-string types."""
    # bytes() should work on types that support it
    IType = NewerType("IType", int)
    i = IType(5)
    # int supports bytes(size) to create zero-filled bytes
    assert bytes(i) == b"\x00\x00\x00\x00\x00"
