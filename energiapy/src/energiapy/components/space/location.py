"""Location where Operations can reside
"""

from __future__ import annotations

from operator import is_
from typing import TYPE_CHECKING, Self

from gana.sets.index import I

from ...utils.dictionary import get_depth
from ..types.scope import ScpCmp

if TYPE_CHECKING:
    from ...represent.space import Space
    from ..commodity.cash import Cash


class Loc(ScpCmp):
    """A discretization of Space"""

    def __init__(self, *has: tuple[Self], label=None):

        self.has: tuple[Self] = has
        self.isin = None
        self.currency: Cash = None
        self.space: Space = None
        self.alsohas: tuple[Self] = ()

        for loc in self.has:
            loc.isin = self
            setattr(self, loc.name, loc)
            for locin in loc.has:
                if not locin in self.has:
                    self.alsohas += (locin,)

        ScpCmp.__init__(self, label)
        self._indexed = False

    def tree(self):
        """Prints the tree of Locations"""
        if self.has:
            return {loc: loc.tree() for loc in self.has}
        return {}

    def depth(self):
        """Finds the depth of the Location"""
        return get_depth(self.tree())

    @property
    def xset(self) -> I:
        """gana index set (I) of Locations"""
        if not self._indexed:
            setattr(self.prg, self.name, I(*[i.name for i in self.has]))
            self._indexed = True
        return getattr(self.prg, self.name)

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

    def all(self):
        """gives locations within"""
        if self.has:
            for loc in self.has:
                yield loc
                yield from loc.all()

    def __add__(self, location: Self):

        if self.name == '':
            # this happens when adding multiple locations
            return Loc(*self.has, location)

        return Loc(location, self)
