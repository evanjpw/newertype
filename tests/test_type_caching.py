"""Tests for type caching added in version 1.0.0."""

from newertype import NewerType


def test_basic_caching():
    """Test that calling NewerType with same parameters returns same type."""
    Type1 = NewerType("MyType", int, use_cache=True)
    Type2 = NewerType("MyType", int, use_cache=True)
    assert Type1 is Type2


def test_different_names_different_types():
    """Test that different names create different types."""
    Type1 = NewerType("Type1", int, use_cache=True)
    Type2 = NewerType("Type2", int, use_cache=True)
    assert Type1 is not Type2


def test_different_wrapped_types_different_types():
    """Test that different wrapped types create different types."""
    IntType = NewerType("MyType", int, use_cache=True)
    StrType = NewerType("MyType", str, use_cache=True)
    assert IntType is not StrType


def test_different_extra_forwards_different_types():
    """Test that different extra_forwards create different types."""
    Type1 = NewerType("MyType", int, extra_forwards=["foo"], use_cache=True)
    Type2 = NewerType("MyType", int, extra_forwards=["bar"], use_cache=True)
    assert Type1 is not Type2


def test_same_extra_forwards_same_type():
    """Test that same extra_forwards (even different order) returns same type."""
    Type1 = NewerType("MyType", int, extra_forwards=["foo", "bar"], use_cache=True)
    Type2 = NewerType("MyType", int, extra_forwards=["bar", "foo"], use_cache=True)
    assert Type1 is Type2


def test_different_no_def_forwards_different_types():
    """Test that different no_def_forwards values create different types."""
    Type1 = NewerType("MyType", int, no_def_forwards=True, use_cache=True)
    Type2 = NewerType("MyType", int, no_def_forwards=False, use_cache=True)
    assert Type1 is not Type2


def test_cached_types_work_correctly():
    """Test that cached types still work correctly."""
    Type1 = NewerType("MyType", int, use_cache=True)
    Type2 = NewerType("MyType", int, use_cache=True)

    # Should be same type
    assert Type1 is Type2

    # Instances should work correctly
    val1 = Type1(42)
    val2 = Type2(99)

    # Both should be instances of the cached type
    assert isinstance(val1, Type1)
    assert isinstance(val1, Type2)
    assert isinstance(val2, Type1)
    assert isinstance(val2, Type2)

    # Operations should work
    assert val1.inner == 42
    assert val2.inner == 99


def test_cache_persistence():
    """Test that cache persists across multiple calls."""
    # Create type
    Type1 = NewerType("CachedType", int, use_cache=True)
    id1 = id(Type1)

    # Create instances
    val1 = Type1(1)
    val2 = Type1(2)

    # Get type again
    Type2 = NewerType("CachedType", int, use_cache=True)
    id2 = id(Type2)

    # Should be same type object
    assert id1 == id2
    assert Type1 is Type2

    # Old instances should still work with new reference
    assert isinstance(val1, Type2)
    assert isinstance(val2, Type2)


def test_use_cache_false():
    """Test that use_cache=False disables caching."""
    Type1 = NewerType("MyType", int, use_cache=False)
    Type2 = NewerType("MyType", int, use_cache=False)

    # Should be different types when caching is disabled
    assert Type1 is not Type2


def test_use_cache_false_with_cached_type():
    """Test that use_cache=False creates new type even if one is cached."""
    # Create and cache a type
    Type1 = NewerType("MyType", int, use_cache=True)

    # Create with use_cache=False should create new type
    Type2 = NewerType("MyType", int, use_cache=False)

    assert Type1 is not Type2

    # Getting cached version should still work
    Type3 = NewerType("MyType", int, use_cache=True)
    assert Type1 is Type3


def test_use_cache_default_is_false():
    """Test that caching is enabled by default."""
    Type1 = NewerType("DefaultCache", int)
    Type2 = NewerType("DefaultCache", int)

    # Default behavior should cache
    assert Type1 is not Type2
