"""Mathematical Program"""

from dataclasses import dataclass, field
from typing import Self

from gurobipy import read as gpread
from IPython.display import display

from ..elements.cons import Cons
from ..elements.func import Func
from ..elements.idx import X
from ..elements.obj import Obj
from ..elements.var import Var
from ..sets.constraint import C
from ..sets.function import F
from ..sets.index import I
from ..sets.parameter import P
from ..sets.variable import V
from .sets import Sets

try:
    from pyomo.environ import ConcreteModel as PyoModel

    has_pyomo = True
except ImportError:
    has_pyomo = False

# from ..value.zero import Z
# from ..sets.ordered import Set

# from ..sets.theta import T


@dataclass
class Prg:
    """A mathematical program"""

    name: str = field(default='prog')
    tol: float = field(default=None)
    canonical: bool = field(default=True)

    def __post_init__(self):
        self.names = []
        self.sets = Sets()
        self.names_idx = []
        self.indices: list[X] = []
        self.variables: list[Var] = []
        # self.thetas: list[Th] = []
        self.functions: list[Func] = []
        self.constraints: list[Cons] = []
        self.objectives: list[Obj] = []

        # is optimized
        self._isopt = False

        # number of:
        self._nx = 0  # index elements
        self._nvar = 0  # variables
        self._nfunc = 0  # functions
        self._ncons = 0  # constraints
        self._nobj = 0  # objectives

    def __setattr__(self, name, value) -> None:

        if isinstance(value, (str, float, int, list, Sets)) or value is None:
            super().__setattr__(name, value)
            return

        if name in self.names:
            if isinstance(value, (I, V, P)) and getattr(self, name).mutable:
                value.mutable = True
            else:
                raise ValueError(f'{self.name}: Overwriting {name}')

        # set objects are set to self.sets
        # .pname is the name given by the user
        # F, C, Obj name are operations they perform

        if isinstance(value, I):
            if not name in self.names:
                self.names.append(name)
                setattr(self.sets, name, value)
                skip_set = False

            else:
                if getattr(self, name).mutable:
                    setattr(self.sets, name, getattr(self, name) | value)
                    skip_set = True
                skip_set = False

            if not value.ordered:
                for n, idx in enumerate(value._):
                    if idx.name in self.names_idx:
                        # if index already declared as part of another index set
                        # update her parent

                        idx = self.indices[self.indices.index(idx)]
                        if not value in idx.parent:
                            idx._parent.append(value)
                            idx._pos.append(n)
                            value._[n] = idx
                    else:
                        setattr(self, idx.name, idx)

            if not skip_set:
                super().__setattr__(name, value)
            return

        elif isinstance(value, V):
            add_len = len(value._)
            add_vars = list(value._)

            if not name in self.names:
                self.names.append(name)
                setattr(self.sets, name, value)
                if value.nn:
                    setattr(self, value.name + '_nn', -value <= 0)
                skip_set = False

            else:

                # the var set is mutable and new vars are being add
                var_ex: V = getattr(self.sets, name)  # existing var set

                if set(value.index).issubset(var_ex.index):
                    return

                for var in value._:
                    # push the positions of the new variables ahead
                    var.pos += len(var_ex._)
                    var.parent = var_ex

                # update the vars and index sets
                var_ex._ += value._
                var_ex.index |= value.index
                var_ex.idx = {idx: var for idx, var in zip(var_ex.index, var_ex._)}

                skip_set = True
                if value.nn:
                    setattr(
                        self,
                        var_ex.name + '_nn',
                        -var_ex(value.index) <= 0,
                    )

            for n, var in enumerate(add_vars):
                var.n = self._nvar + n

            self._nvar += add_len

            self.variables += add_vars
            if not skip_set:
                super().__setattr__(name, value)
            return

        elif isinstance(value, P):
            add_len = len(value._)

            if not name in self.names:
                self.names.append(name)
                setattr(self.sets, name, value)
                skip_set = False
            else:
                par_ex: P = getattr(self.sets, name)

                if set(value.index).issubset(par_ex.index):
                    return

                par_ex._ += value._
                par_ex.index |= value.index
                par_ex.idx = {idx: par for idx, par in zip(par_ex.index, par_ex._)}

                skip_set = True

            if not skip_set:
                super().__setattr__(name, value)
            return

        elif isinstance(value, F):
            setattr(self.sets, name, value)
            value.pname = name
            self.functions += value._

            for n, f in enumerate(value._):
                f.n = self._nfunc + n

            self._nfunc += len(value._)

            super().__setattr__(name, value)
            return

        elif isinstance(value, C):
            setattr(self.sets, name, value)
            value.pname = name
            self.constraints += value._

            for n, c in enumerate(value._):
                c.n = self._ncons + n

            self._ncons += len(value._)

            super().__setattr__(name, value)
            return

        elif isinstance(value, Obj):
            self.names.append(name)
            value.pname = name
            value.n = self._nobj
            self._nobj += 1
            self.objectives.append(value)

            super().__setattr__(name, value)
            return

        elif isinstance(value, X):
            value.n = self._nx
            self._nx += 1
            self.indices.append(value)
            self.names_idx.append(value.name)

            super().__setattr__(name, value)
            return

        super().__setattr__(name, value)

    def vardict(self) -> dict[V, Var]:
        """Variables"""
        return {v: v._ for v in self.sets.variable}

    def nncons(self, n: bool = False) -> list[int | Cons]:
        """non-negativity constraints"""
        if n:
            return [x.n for x in self.constraints if x.nn]
        return [x for x in self.constraints if x.nn]

    def eqcons(self, n: bool = False) -> list[int | Cons]:
        """equality constraints"""
        if n:
            return [x.n for x in self.constraints if not x.leq]
        return [x for x in self.constraints if not x.leq]

    def leqcons(self, n: bool = False) -> list[int | Cons]:
        """less than or equal constraints"""
        if n:
            return [x.n for x in self.constraints if x.leq and not x.nn]
        return [x for x in self.constraints if x.leq and not x.nn]

    def cons(self, n: bool = False) -> list[int | Cons]:
        """constraints"""
        return self.leqcons(n) + self.eqcons(n) + self.nncons(n)

    def nnvars(self, n: bool = False) -> list[int | Var]:
        """non-negative variables"""
        if n:
            return [x.n for x in self.variables if x.nn]
        return [x for x in self.variables if x.nn]

    def bnrvars(self, n: bool = False) -> list[int | Var]:
        """binary variables"""
        if n:
            return [x.n for x in self.variables if x.bnr]
        return [x for x in self.variables if x.bnr]

    def intvars(self, n: bool = False) -> list[int | Var]:
        """integer variables"""
        if n:
            return [x.n for x in self.variables if x.itg]
        return [x for x in self.variables if x.itg]

    def contvars(self, n: bool = False) -> list[int | Var]:
        """continuous variables"""
        if n:
            return [x.n for x in self.variables if not x.bnr and not x.itg]
        return [x for x in self.variables if not x.bnr and not x.itg]

    def B(self, zero: bool = True) -> list[float | None]:
        """RHS Parameter vector"""
        return [c.func.B(zero) for c in self.cons()]

    def A(self, zero: bool = True) -> list[list[float | None]]:
        """Matrix of Variable coefficients"""
        a_ = []

        for c in self.cons():
            if zero:
                row = [0] * len(self.contvars())
            else:
                row = [None] * len(self.contvars())
            for n, value in zip(c.X(), c.A()):
                row[n] = value
            a_.append(row)
        return a_

    def _A(self) -> list[list[float]]:
        """Matrix of Variable coefficients"""
        a_ = []

        for c in self.constraints:
            row = [0] * len(self.contvars())
            for n, value in zip(c.X(), c.A()):
                row[n] = value
            a_.append(row)
        return a_

    def C(self, zero: bool = True) -> list[float]:
        """Objective Coefficients"""
        c_ = []

        for o in self.objectives:
            if zero:
                row = [0] * len(self.contvars())
            else:
                row = [None] * len(self.contvars())

            for n, value in zip(o.X(), o.A()):
                row[n] = value
            c_.append(row)
        if len(self.objectives) == 1:
            return c_[0]
        return c_

    def matrix(
        self, zero: bool = False
    ) -> tuple[list[list[float | None]], list[float | None]]:
        """Matrix Representation"""
        return self.A(zero), self.B(zero)

    def X(self) -> list[list[int]]:
        """Structure of the constraint matrix"""
        return [c.X() for c in self.constraints]

    def G(self, zero: bool = True) -> list[float | None]:
        """Matrix of Variable coefficients for type:

        g < = 0
        """
        g_ = []

        for c in self.leqcons():
            if zero:
                row = [0] * len(self.contvars())
            else:
                row = [None] * len(self.contvars())
            for n, value in zip(c.X(), c.A()):
                row[n] = value
            g_.append(row)
        return g_

    def H(self, zero: bool = True) -> list[float | None]:
        """Matrix of Variable coefficients for type:

        h = 0
        """
        h_ = []

        for c in self.eqcons():
            if zero:
                row = [0] * len(self.contvars())
            else:
                row = [None] * len(self.contvars())
            for n, value in zip(c.X(), c.A()):
                row[n] = value
            h_.append(row)
        return h_

    def NN(self, zero: bool = True) -> list[float | None]:
        """Matrix of Variable coefficients for non negative cons"""
        nn_ = []

        for c in self.nncons():
            if zero:
                row = [0] * len(self.contvars())
            else:
                row = [None] * len(self.contvars())
            for n, value in zip(c.X(), c.A()):
                row[n] = value
            nn_.append(row)
        return nn_

    def pyomo(self):
        """Pyomo Model"""
        if has_pyomo:
            m = PyoModel()

            for s in self.sets.index:
                setattr(m, s.name, s.pyomo())

            for v in self.sets.variable:
                setattr(m, v.name, v.pyomo())

            # for p in self.parsets:
            #     setattr(m, p.name, p.pyomo())

            # for c in self.conssets:
            #     setattr(m, c.name, c.pyomo(m))

            return m
        print(
            'pyomo is an optional dependency, pip install gana[all] to get optional dependencies'
        )

    def mps(self, name: str = None):
        """MPS File"""
        ws = ' '
        with open(f'{name or self.name}.mps', 'w', encoding='utf-8') as f:
            f.write(f'NAME{ws*10}{self.name.upper()}\n')
            f.write('ROWS\n')
            f.write(f'{ws}N{ws*3}{self.objectives[0].mps()}\n')
            for c in self.leqcons():
                f.write(f'{ws}L{ws*3}{c.mps()}\n')
            for c in self.eqcons():
                f.write(f'{ws}E{ws*3}{c.mps()}\n')
            f.write('COLUMNS\n')
            for v in self.variables:
                vs = len(v.mps())
                for c in v.features:
                    vfs = len(c.mps())
                    f.write(ws * 4)
                    f.write(v.mps())
                    f.write(ws * (10 - vs))
                    f.write(c.mps())
                    f.write(ws * (10 - vfs))
                    if isinstance(c, Obj):
                        f.write(f'{self.C()[v.n]}')
                    else:
                        f.write(f'{self._A()[c.n][v.n]}')
                    f.write('\n')

            f.write('RHS\n')
            for n, c in enumerate(self.leqcons() + self.eqcons()):
                f.write(ws * 4)
                f.write(f'RHS{n}')
                f.write(ws * (10 - len(f'RHS{n+1}')))
                f.write(c.mps())
                f.write(ws * (10 - len(c.mps())))
                f.write(f'{c.B()}')
                f.write('\n')
            f.write('ENDATA')

    def gurobi(self):
        """Gurobi Model"""
        self.mps()
        return gpread(f'{self.name}.mps')

    def lp(self):
        """LP File"""
        m = self.gurobi()
        m.write(f'{self.name}.lp')

    def opt(self, using: str = 'gurobi'):
        """Solve the program"""

        if using == 'gurobi':
            m = self.gurobi()
            m.optimize()
            vals = [v.X for v in m.getVars()]
            for v, val in zip(self.variables, vals):
                v._ = val

            for f in self.functions:
                f.eval()

        self._isopt = True

    def vars(self):
        """Optimal Variable Values"""
        return {v: v._ for v in self.variables}

    def obj(self):
        """Objective Values"""
        if len(self.objectives) == 1:
            return self.objectives[0]._
        return {o: o._ for o in self.objectives}

    def slack(self):
        """Slack in each constraint"""
        return {c: c._ for c in self.leqcons()}

    def sol(self):
        """Print sol"""

        if not self._isopt:
            return r'Use .opt() to generate solution'

        print(rf'Solution for {self.name}')
        print()
        print(r'---Objective Value(s)---')
        print()
        for o in self.objectives:
            o.sol()

        print()
        print(r'---Variable Value---')
        print()

        for v in self.variables:
            v.sol()

        print()
        print(r'---Constraint Slack---')
        print()

        for c in self.leqcons() + self.eqcons():
            c.sol()

    # Displaying the program
    def latex(self, descriptive: bool = False):
        """Display LaTeX"""

        for s in self.sets.index:
            display(s.latex(True))

        for o in self.objectives:
            display(o.latex())

        if descriptive:
            for c in self.cons():
                display(c.latex())

        else:
            for c in self.sets.cons():
                display(c.latex())

            for c in self.cons():
                if not c.parent:
                    display(c.latex())

    def pprint(self, descriptive: bool = False):
        """Pretty Print"""

        print(rf'Mathematical Program for {self.name}')

        if self.sets.index:
            print()
            print(r'---Index Sets---')
            print()

            for i in self.sets.index:
                i.pprint(True)

        if self.objectives:
            print()
            print(r'---Objective(s)---')
            print()

            for o in self.objectives:
                o.pprint()

        print()
        print(r'---Such that---')
        print()

        if descriptive:
            for c in self.cons():
                c.pprint()

        else:
            for c in self.sets.cons():
                c.pprint()

    def __str__(self):
        return rf'{self.name}'

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(str(self))

    def __add__(self, other: Self):
        """Add two programs"""

        if not isinstance(other, Prg):
            raise ValueError('Can only add programs')

        prg = Prg(name=rf'{self.name}')

        for i in (
            self.sets.index
            + other.sets.index
            + self.sets.variable
            + other.sets.variable
            + self.sets.parameter
            + other.sets.parameter
        ):
            if not i.name in prg.names:
                setattr(prg, i.name, i)
            else:
                if isinstance(i, I) and i.mutable:
                    setattr(prg, i.name, getattr(prg, i.name) | i)

        for i in (
            self.sets.function
            + other.sets.function
            + self.sets.leqcons()
            + self.sets.eqcons()
            + other.sets.leqcons()
            + other.sets.eqcons()
            + self.objectives
            + other.objectives
        ):
            if not i.name in prg.names:
                setattr(prg, i.name, i)

        return prg
