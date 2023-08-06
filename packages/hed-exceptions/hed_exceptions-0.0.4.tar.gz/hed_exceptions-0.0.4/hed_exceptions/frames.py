"""Helper module for retrieval of stack-frames info during runtime."""
from inspect import FrameInfo
from inspect import currentframe
from inspect import getframeinfo
from typing import Optional

__all__ = [
    "get_caller",
    "get_creation",
]


def _frame2info(frame) -> Optional[FrameInfo]:
    """Creates and return FrameInfo namedtuple from a frame."""

    return FrameInfo(frame, *getframeinfo(frame)) if frame else None


def get_caller(calls_back=1) -> Optional[FrameInfo]:
    """Returns the calling method's caller's (caller's) FrameInfo."""

    skip_frames = calls_back + 1  # +1 for calling this method itself
    frame = currentframe()
    while frame and skip_frames > 0 and frame.f_back:
        frame = frame.f_back
        skip_frames -= 1
    return _frame2info(frame)


def get_creation(self) -> Optional[FrameInfo]:
    """Call this from __init__ to get FrameInfo for the context of creation.

    Note:
        This method accounts for inheritance and constructors chaining.
    """

    init_frame = None
    f = currentframe()
    while f:
        in_self = ("self" in f.f_locals) and (self is f.f_locals["self"])
        in_init_method = f.f_code.co_name == "__init__"
        if in_init_method and in_self:
            init_frame = f
        f = f.f_back

    return _frame2info(init_frame.f_back) if init_frame else None
