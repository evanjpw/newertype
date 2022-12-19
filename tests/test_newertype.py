import pytest

from newertype import NewerType


def test_basic():
    AType = NewerType("AType", int)  # noqa: N802
    a_type = AType(14)
    assert isinstance(a_type, AType)
    assert a_type.inner == 14
    a_type.inner = 27
    assert a_type.inner == 27
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
        assert bytes(s_type) == b""
    assert "cannot convert 'float' object to bytes" in str(e)
    s_type.inner = 0.0
    assert bool(s_type) is False
    assert s_type is not None


def test_forwarding():
    IType = NewerType("IType", int)  # noqa: N802
    i_type_1 = IType(7)
    i_type_2 = IType(14)
    i_result = i_type_1.__add__(i_type_2)
    assert i_result == 21
    assert int(i_type_1) < int(i_type_2)
    assert i_type_1 + i_type_2 == 21
    JType = NewerType("JType", int)  # noqa: N802
    j_type_1 = JType(7)
    with pytest.raises(TypeError) as e:
        assert i_type_1 + j_type_1 == 21
    assert "unsupported operand type(s) for +: 'IType' and 'JType'" in str(e)
