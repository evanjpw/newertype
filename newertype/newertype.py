from typing import Any, Generic, Type, TypeVar

__all__ = ["NewerType"]

T = TypeVar("T")


class NewerTypeType(type):
    """"""

    def __new__(mcs, _name, bases, namespace, **kwargs):
        name = kwargs.get("name", _name)
        contained_type = kwargs.get("the_contained_type", Any)
        namespace["contained_type"] = contained_type
        return super().__new__(mcs, name, bases, namespace)


def NewerType(name: str, the_contained_type: Type[T], **kwargs) -> type:  # noqa: N802
    """"""

    class NewerTypeInstance(Generic[T], metaclass=NewerTypeType, name=name, the_contained_type=the_contained_type):
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
        def deref(self) -> T:
            return self._contents

        @deref.setter
        def deref(self, value: T) -> None:
            self._contents = value

    return NewerTypeInstance
# J = TypeVar("J")
# *argsIIIIIIIJJparent_typeparent_typeparent_type: "NewerType[T]",
#  = parent_type.
# classGeneric[T]JparentJ"Newer"class_dictclass_dict
        # _contained_type: Type[T]J
            # self
    # name: str
    # the_contained_type: Type[T]
    #
    # def __init__(self, ) -> None:
    #     self.name = name
    #     self.the_contained_type = the_contained_type
    #
    # def __call__(self, *args, **kwargs) -> NewerTypeInstance:
    #     """"""
    #     return NewerTypeInstance(self, *args, **kwargs)




