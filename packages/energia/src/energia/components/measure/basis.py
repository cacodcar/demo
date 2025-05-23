"""Unit"""

from operator import is_
from typing import Self

from ..core.tag import Name


class Unit(Name):
    """Unit of measure for a quantity provided as input to a component"""

    def __init__(self, basis: Self = None, times: int | float = None, label=None):
        # A basis can itself be measured using another basis
        self.basis = basis
        # How many times that basis is self?
        self.times = times

        Name.__init__(self, label)

    def howmany(self, basis: Self):
        """How many times is this basis contained in the other basis"""
        if is_(basis, self.basis):
            return self.times

        elif is_(self, basis.basis):
            return basis.times

        elif is_(self.basis, basis.basis):
            return self.times / basis.times

        raise ValueError(
            f"{self} and {basis} do not have a common basis for comparison"
        )

    # can only be divided/multiplied by a number
    def __truediv__(self, other: float):

        if isinstance(other, Unit):
            return self.howmany(other)

        elif isinstance(other, (int, float)):
            if self.basis:
                b = Unit(
                    self.basis,
                    1 / (other * self.times),
                    f'{self.label}/{other*self.times}',
                )
            else:
                b = Unit(self, 1 / other, f'{self.label}/{other}')
                self.basis = b
                self.times = other
            return b

    def __mul__(self, other: float):
        if not isinstance(other, (int, float)):
            raise TypeError(f"Cannot multiply Unit by {type(other)}")
        if self.basis:
            b = Unit(
                self.basis, other * self.times, f'{self.label}.{other*self.times}'
            )
        else:
            b = Unit(self, other, f'{self.label}.{other}')
            self.basis = b
            self.times = 1 / other
        return b

    def __rmul__(self, other: float):
        return self * other
