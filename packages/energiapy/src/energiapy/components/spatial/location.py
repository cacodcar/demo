"""Location where Operations can reside
"""

from __future__ import annotations

from operator import is_
from typing import TYPE_CHECKING, Self

from gana.sets.index import I

from ...utils.dictionary import get_depth
from .._core.sample import Index
from .linkage import Link

if TYPE_CHECKING:
    from ...modeling.space import Space
    from ..commodity.misc import Cash


class Loc(Index):
    """A discretization of Space"""

    def __init__(self, *has: tuple[Self], label=None):

        Index.__init__(self, label=label)

        self.has: tuple[Self] = has
        self.isin = None
        self.currency: Cash = None
        self.space: Space = None
        self.alsohas: tuple[Self] = ()

        for loc in self.has:
            if loc.name:
                loc.isin = self
                setattr(self, loc.name, loc)
                for locin in loc.has:
                    if not locin in self.has:
                        self.alsohas += (locin,)

    def tree(self):
        """Prints the tree of Locations"""
        if self.has:
            return {loc: loc.tree() for loc in self.has}
        return {}

    def depth(self):
        """Finds the depth of the Location"""
        return get_depth(self.tree())

    def __setattr__(self, name, value):

        if name == 'currency' and value:
            # all locations in the location have the same currency
            for loc in self.has + self.alsohas:
                loc.currency = value

        super().__setattr__(name, value)

    def sink(self):
        """Tells whether the location is a sink"""
        if self in self.space.sinks:
            return True
        return False

    def source(self):
        """Tells whether the location is a source"""
        if self in self.space.sources:
            return True
        return False

    def links(self, location, print_link: bool = True) -> list:
        """Finds the links between two Locations

        Args:
            location (IsLocation): Location to find links with
            print_link (bool, optional): Whether the links are to be printed. Defaults to True.

        Returns:
            list: Provides the links between the locations
        """
        links = []
        for link in self.space.links:
            source, sink = False, False

            if is_(self, link.source) and is_(location, link.sink):
                source, sink = self, location

            if is_(self, link.sink) and is_(location, link.source):
                source, sink = location, self

            if source and sink:
                links.append(link)
                if print_link:
                    print(f'{source} is source and {sink} is sink in {link}')
                continue
        return links

    def connected(self, location, print_link: bool = False) -> bool:
        """Finds whether the Locations are connected
        Args:
            location (IsLocation): Location to verify Links with
            print_link (bool, optional): Whether to print the Links. Defaults to False.

        Returns:
            bool: True if Locations are connection
        """
        if self.links(location, print_link=print_link):
            return True
        return False

    def all(self):
        """gives locations within"""
        if self.has:
            for loc in self.has:
                yield loc
                yield from loc.all()

    def __add__(self, location: Self):
        """Creates another location which consists of self and other"""
        if not self.name:
            # this happens when adding multiple locations
            return Loc(*self.has, location)
        return Loc(location, self)

    def __radd__(self, number: int):
        """For allowing sum([Loc])"""
        if isinstance(number, int) and number == 0:
            return self

    def __sub__(self, location: Self):
        """Creates a linkage"""
        return Link(source=self, sink=location)

    def __eq__(self, other: Self):
        return is_(self, other)
