"""Component"""


class BscCmp:
    """A component"""

    def __init__(self, label=None):
        # set by the Model
        self.name = ''
        self.label = label

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def __init_subclass__(cls):
        cls.__repr__ = BscCmp.__repr__
        cls.__hash__ = BscCmp.__hash__

    # def disp(self, loc: Loc = None, time: Period = None):
    #     """Generates a disposition, if not user-provided"""

    #     if loc:
    #         loc = loc.x
    #     else:
    #         # if loc is not defined
    #         # take the set of all locations
    #         loc = self.mdl.prg.locs

    #     if time:
    #         time = time.xset
    #     else:
    #         # if no temporal index
    #         # get the densest time index
    #         time = self.mdl.time.densest.x
    #     return loc, time

    # def var(
    #     self,
    #     name: str,
    #     loc: Loc = None,
    #     time: Period = None,
    # ) -> V:
    #     """(set and) return an independent variable"""

    #     loc, time = self.disp(loc, time)

    #     setattr(
    #         self.prg,
    #         name,
    #         V(
    #             self.x,
    #             loc,
    #             time,
    #             mutable=True,
    #         ),
    #     )
    #     return getattr(self.prg, name)(self.x, loc, time)

    # def var_calc(
    #     self, var: str, comp_dep: DefCmp, loc: Loc = None, time: Period = None
    # ) -> V:
    #     """(set and) return a calculated (dependent) variable"""
    #     loc, time = self.disp(loc, time)
    #     setattr(
    #         self.prg,
    #         var,
    #         V(
    #             self.x,
    #             comp_dep.x,
    #             loc,
    #             time,
    #             mutable=True,
    #         ),
    #     )
    #     return getattr(self.prg, var)(self.x, comp_dep.x, loc, time)

    # def par(self, attr: str, info: list, loc: Loc = None, time: Period = None) -> P:
    #     """(set and return) a parameter"""
    #     loc, time = self.disp(loc, time)

    #     setattr(
    #         self.prg,
    #         attr,
    #         P(
    #             self.x,
    #             loc,
    #             time,
    #             _=info,
    #             mutable=True,
    #         ),
    #     )
    #     return getattr(self.prg, attr)(self.x, loc, time)

    # @property
    # def index(self):
    #     """Index set"""
    #     if not self._indexed:
    #         setattr(self.prg, self.name, I(self.name))
    #         self._indexed = True
    #     return getattr(self.prg, self.name)

    # @property
    # def x(self):
    #     """gana index element (X)"""
    #     return getattr(self.mdl.prg, self.name)

    # @property
    # def _(self):
    #     """gana index set (I)"""
    #     return self.index

    # @property
    # def model(self):
    #     """The model for the Component"""
    #     return self.mdl

    # @property
    # def program(self):
    #     """The program for the Component"""
    #     return self.prg

    # def bound(self, var: str, loc: Loc, time: Period):
    #     """Bound a component attribute"""
    #     return Bound(comp=self, var=var, loc=loc, time=time)

    # def calculate(
    #     self, var_calc: str, var_dep: str, comp_dep: DefCmp, loc: Loc, time: Period
    # ):
    #     """Calculate a component attribute"""

    #     return Calculate(
    #         comp=self,
    #         var_calc=var_calc,
    #         comp_dep=comp_dep,
    #         var_dep=var_dep,
    #         loc=loc,
    #         time=time,
    #     )

    # def pprint(self, descriptive: bool = False):
    #     """Pretty print"""
    #     self.prg.pprint(descriptive)
