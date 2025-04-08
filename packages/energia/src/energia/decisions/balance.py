"""Bal"""

from __future__ import annotations

from dataclasses import dataclass
from operator import is_
from typing import TYPE_CHECKING

from ..components.core.tag import Name
from ..components.temporal.lag import Lag

if TYPE_CHECKING:
    from gana.block.program import Prg

    from ..components.commodity.resource import Resource
    from ..components.measure.basis import Unit
    from ..components.operation.process import Process
    from ..components.operation.storage import Storage
    from ..modeling.model import Model


@dataclass
class Bal(Name):
    """Process converts one Resource to another Resource"""

    process: Process = None
    storage: Storage = None
    resource: Resource = None

    def __post_init__(self):
        Name.__post_init__(self)

        if self.process:
            self.operation = self.process
        elif self.storage:
            self.operation = self.storage

        self.name = f'η({self.process})'
        self.base: Resource = None
        self.balance: dict[Resource : int | float] = {}
        self.lag: Lag = None

    @property
    def model(self) -> Model:
        """energia Model"""
        return self.operation.model

    @property
    def program(self) -> Prg:
        """gana Program"""
        return self.operation.program

    def __getitem__(self, lag: Lag):
        if isinstance(lag, Lag):
            self.lag = lag
            return self

    def __call__(self, thing: Resource | Bal):
        """Bal is called with a Resource to be converted"""

        if isinstance(thing, Bal):
            self.balance = {**self.balance, **thing.balance}
            self.base = list(self.balance)[0]
        else:
            self.base = thing
            self.balance = {thing: 1.0, **self.balance}

        # self.operation.operate.V(1) == 1.0 * self.base.produce.V(1)
        # setattr(self.program, f''
        return self

    def __eq__(self, other: Bal | float):
        # cons = []
        if isinstance(other, (int, float)):
            # this is used for inventory balance
            self.balance = {**self.balance, self.resource: -1 / float(other)}
        else:
            # this is when there is a proper resource balance
            # -20*res1 = 10*res2 for example
            self.balance: dict[Resource, int | float] = {
                **self.balance,
                **other.balance,
            }
        self.model.balance[self.operation] = self.balance
        give_ = []
        take_ = []

        for res, par in self.balance.items():
            # set, the balance on the resource
            setattr(res, self.name, self)
            # now there are two cases possible
            # the parameter (par) is positive or negative
            # if positive, the resource is consumed
            # if negative, the resource is produced
            # also, the par can be an number or a list of numbers

            if isinstance(par, (int | float)) and par < 0:
                # condition: negative number
                if self.lag:
                    take_.append(
                        -par * self.model.consume(res, self.operation, self.lag).V(par)
                    )
                else:

                    take_.append(-par * self.model.consume(res, self.operation).V(par))

            elif isinstance(par, list) and par[0] < 0:
                # condition: list with negative numbers
                # TODO: cant handle numbers that go both ways
                if self.lag:
                    take_.append(
                        [-i for i in par]
                        * self.model.consume(res, self.operation, self.lag).V(par)
                    )
                else:
                    take_.append(
                        [-i for i in par]
                        * self.model.consume(res, self.operation).V(par)
                    )

            else:
                # condition: positive number
                if self.lag:
                    give_.append(
                        par
                        * self.model.produce(res, self.operation, self.lag.of).V(par)
                    )

                else:

                    give_.append(par * self.model.produce(res, self.operation).V(par))

        # inventory(resource) <= setup(storage)
        if self.storage:
            setattr(
                self.program,
                f'{self.storage}_inventory_UB',
                self.storage.inventory(self.base).V(length=len(self.model.time.densest))
                <= self.storage.setup.V(length=len(self.model.horizon)),
            )
            self.storage.constraints.append(f'{self.storage}_inventory_UB')
            self.base.constraints.append(f'{self.storage}_inventory_UB')

    def __add__(self, other: Bal):
        if isinstance(other, Bal):
            self.balance = {**self.balance, **other.balance}
            return self
        self.balance = {**self.balance, other: 1}
        return self

    def __sub__(self, other: Bal):
        if isinstance(other, Bal):
            self.balance = {
                **self.balance,
                **{res: -1 * par for res, par in other.balance.items()},
            }
            return self
        self.balance = {**self.balance, other: -1}
        return self

    def __mul__(self, times: int | float | list):
        if isinstance(times, list):
            self.balance = {
                res: [par * i for i in times] for res, par in self.balance.items()
            }
        else:
            self.balance = {res: par * times for res, par in self.balance.items()}
        return self

    def __rmul__(self, times):
        return self * times
