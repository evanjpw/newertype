from typing import Any, Dict, Generic, List, Type, TypeVar

# import pdb

__all__ = ["NewerType"]

T = TypeVar("T")


class NewerTypeType(type):
    """"""

    METHODS_TO_FORWARD: List[str] = [
        "__len__",
        "__length_hint__",
        "__getitem__",
        "__setitem__",
        "__delitem__",
        "__missing__",
        "__iter__",
        "__reversed__",
        "__contains__",
        "__add__",
        "__sub__",
        "__mul__",
        "__matmul__",
        "__truediv__",
        "__floordiv__",
        "__mod__",
        "__divmod__",
        "__pow__",
        "__lshift__",
        "__rshift__",
        "__and__",
        "__xor__",
        "__or__",
        "__radd__",
        "__rsub__",
        "__rmul__",
        "__rmatmul__",
        "__rtruediv__",
        "__rfloordiv__",
        "__rmod__",
        "__rdivmod__",
        "__rpow__",
        "__rlshift__",
        "__rrshift__",
        "__rand__",
        "__rxor__",
        "__ror__",
        "__iadd__",
        "__isub__",
        "__imul__",
        "__imatmul__",
        "__itruediv__",
        "__ifloordiv__",
        "__imod__",
        "__ipow__",
        "__ilshift__",
        "__irshift__",
        "__iand__",
        "__ixor__",
        "__ior__",
        "__neg__",
        "__pos__",
        "__abs__",
        "__invert__",
        "__complex__",
        "__int__",
        "__float__",
        "__index__",
        "__round__",
        "__trunc__",
        "__floor__",
        "__ceil__",
        "__enter__",
        "__exit__",
        "__eq__",
        "__le__",
        "__lt__",
        "__gt__",
        "__ge__",
    ]

    def __new__(mcs, _name, bases, namespace, **kwargs):
        contained_type = kwargs.get("the_contained_type", Any)
        namespace["contained_type"] = contained_type
        name = kwargs.get("class_name", _name)
        return super().__new__(mcs, name, bases, namespace)

    def __init__(cls, name, bases, namespace, **kwargs):
        # print(f"__init__ type is {type(cls)}")
        NewerTypeType._forward_methods(cls, namespace)
        super().__init__(name, bases, namespace)

    @staticmethod
    def _collect_forwardable_methods(contained_type: type) -> List[str]:
        contained_dict = contained_type.__dict__
        # print(f"contained type: {repr(contained_dict)}")
        to_forward = [
            k for k in contained_dict if k in NewerTypeType.METHODS_TO_FORWARD
        ]
        # print(f"to forward is {to_forward}")
        return to_forward

    @staticmethod
    def _forward(cls, method_name, namespace):
        def forwarded(self, *args, **kwargs):
            # print(
            #     f"forward({repr(args)}, {repr(kwargs)}), method_name is {method_name}"
            # )
            # print(f"args types are {[repr(type (arg)) for arg in args]}")
            cooked_args = [  # s
                arg.inner if isinstance(arg, type(self)) else arg for arg in args
            ]
            # print(f"cooked_args is {repr(cooked_args)}, type is {type(self)}")
            method = getattr(self._contents, method_name)
            # print(f"forward method is {repr(method)}")
            # pdb.set_trace()
            value = method(*cooked_args, **kwargs)
            # print(f"value is {value}")
            return value

        setattr(cls, method_name, forwarded)
        # namespace[method_name] = forwarded

    @staticmethod
    def _forward_methods(cls, namespace: Dict[str, Any]) -> None:
        contained_type: type = namespace["contained_type"]
        to_forward = NewerTypeType._collect_forwardable_methods(contained_type)
        for method in to_forward:
            NewerTypeType._forward(cls, method, namespace)
        # print(f"cls.__dict__ is {cls.__dict__}")


def NewerType(name: str, the_contained_type: Type[T], **kwargs) -> type:  # noqa: N802
    """"""

    class NewerTypeInstance(
        Generic[T],
        metaclass=NewerTypeType,
        class_name=name,
        the_contained_type=the_contained_type,
    ):
        """"""

        _contents: T

        def __init__(self, *args, **kwargs) -> None:
            self._contents = the_contained_type(*args, **kwargs)
            super().__init__()  # I would have thought `*args, **kwargs` would work here

        def __str__(self):
            return f"{self.__class__.__name__}({str(self._contents)})"

        def __repr__(self):
            return str(self)

        def __bool__(self):
            return bool(self._contents)

        def __bytes__(self):
            return bytes(self._contents)

        @property
        def inner(self) -> T:
            return self._contents

        @inner.setter
        def inner(self, value: T) -> None:
            # print(f"In setter, values is {value}")
            self._contents = value

    # print(f"NewerTypeInstance.__dict__ is {NewerTypeInstance.__dict__}")

    return NewerTypeInstance
