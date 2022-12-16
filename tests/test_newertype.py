import pytest

from newertype import NewerType


def test_basic():
    AType = NewerType("AType", int)  # noqa: N802
    a_type = AType(14)
    assert isinstance(a_type, AType)
    assert a_type.deref == 14
    a_type.deref = 27
    assert a_type.deref == 27
    assert str(a_type.__class__.__name__) == "AType"
    EType = NewerType("EType", int)  # noqa: N802
    e_type = EType(70)
    assert str(e_type.__class__.__name__) == "EType"
    assert str(a_type.__class__.__name__) == "AType"


def test_string_conversions():
    SType = NewerType("SType", float)  # noqa: N802
    s_type = SType(2.71828182845904523536028747135266249775724709369995)
    assert str(s_type) == "SType(2.718281828459045)"
    assert repr(s_type) == "SType(2.718281828459045)"
    assert bool(s_type) is True
    assert s_type is not None
    with pytest.raises(TypeError) as e:
        assert bytes(s_type) == b"cannot convert 'float' object to bytes"
    assert "" in str(e)
    s_type.deref = 0.0
    assert bool(s_type) is False
    assert s_type is not None
