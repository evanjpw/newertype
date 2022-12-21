from collections import UserDict

import pytest

from newertype import NewerType


def test_custom_forwarding():
    class Forwardable(UserDict):
        def forwarded(self, value):
            return value

        def also_forwarded(self, key):
            return self[key]

        def __getitem__(self, item):
            return super().__getitem__(item)

        def __setitem__(self, key, value):
            super().__setitem__(key, value)

    FO1Type = NewerType("FO1Type", Forwardable)  # noqa: N802
    fo1_type_1 = FO1Type(Forwardable())
    fo1_type_1["a"] = 5
    assert fo1_type_1["a"] == 5
    with pytest.raises(AttributeError) as e:
        assert fo1_type_1.forwarded(5) == 5
    assert "FO1Type' object has no attribute 'forwarded'" in str(e)
    FO2Type = NewerType(
        "FO2Type", Forwardable, extra_forwards=["forwarded", "also_forwarded"]
    )  # noqa: N802
    fo2_type_1 = FO2Type(Forwardable())
    fo2_type_1["e"] = 7
    assert fo2_type_1["e"] == 7
    assert fo2_type_1.also_forwarded("e") == 7
    FO3Type = NewerType(
        "FO3Type", Forwardable, extra_forwards=["also_forwarded"], no_def_forwards=True
    )  # noqa: N802
    fo3_type_1 = FO3Type(Forwardable())
    fo3_type_1.inner["g"] = 8
    assert fo3_type_1.also_forwarded("g") == 8
    with pytest.raises(TypeError) as e:
        assert fo3_type_1["g"] == 8
    assert "'FO3Type' object is not subscriptable" in str(e)
    SEType = NewerType("SEType", str, no_def_forwards=True)  # noqa: N802
    se_type = SEType("`bytes()` always forwards")
    assert bytes(se_type) == b"`bytes()` always forwards"
