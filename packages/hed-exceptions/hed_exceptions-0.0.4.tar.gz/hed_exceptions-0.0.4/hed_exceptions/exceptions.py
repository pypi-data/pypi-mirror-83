from collections import namedtuple

from hed_exceptions import frames

__all__ = [
    "Arg",
    "ArgumentError",
]

Arg = namedtuple("Arg", "name type value")


class ArgumentError(Exception):
    """Easily include argument details without much typing.

     Pass the arg-name to constructor and it's value is retrieved from stack."""

    def __init__(self, name: str, msg="Bad arg!"):
        if not isinstance(name, str):
            raise TypeError(name)
        if not name:
            raise ValueError(name)
        value = frames.get_creation(self).frame.f_locals[name]
        arg = Arg(name, type(value), value)
        super().__init__(msg, arg)
        self.msg = msg
        self.arg = arg

    def __repr__(self):
        return f"{type(self).__name__}({self.msg!r}, {self.arg!r})"

    def __str__(self):
        return repr(self)
