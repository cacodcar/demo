"""Operators"""

from __future__ import annotations
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from ..sets.variable import V
    from ..sets.function import F
    from ..sets.index import I


def sigma(vs: V, hold: I, over: I, hold_right: I = None) -> None:
    """Summation"""
    if hold_right:
        func: F = sum(vs(*hold, idx, hold_right) for idx in over)
        func.issum = (vs, hold, over, hold_right)
    else:
        func: F = sum(vs(*hold, idx) for idx in over)
        func.issum = (vs, hold, over)
    return func


# def pi(vs: V, hold: I, over: I) -> None:
#     """Product"""

#     func: F = prod(vs(*hold, idx) for idx in over)
#     func.isprod = True
#     return func
