# -*- coding: utf-8 -*-

from functools import update_wrapper
from types import MethodType
from typing import Any, Callable, Generic, Optional, Type, TypeVar, Union

from simplethread.thread import start

__all__ = ("threaded",)

_F = TypeVar("_F", bound=Callable[..., Any])


class threaded(Generic[_F]):
    """
    A decorator to run a ``user_function`` in a separate thread.
    """
    def __init__(self, user_function: _F) -> None:
        if not callable(user_function) and not hasattr(user_function, "__get__"):
            raise TypeError(f"{user_function!r} is not callable or a descriptor")

        self.original_function: _F = user_function
        update_wrapper(self, user_function)

    def __call__(self, *args: Any, **kwargs: Any) -> int:
        return start(self.original_function, args, kwargs)

    def __get__(self, instance: Any, owner: Optional[Type[Any]] = None) -> Union["threaded[_F]", MethodType]:
        # Bind a function to an object.
        # Documentation: https://docs.python.org/3/howto/descriptor.html#functions-and-methods
        return self if instance is None else MethodType(self, instance)
