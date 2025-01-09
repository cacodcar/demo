"""Process converts one Resource to another Resource
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING
from .task import Task


if TYPE_CHECKING:
    from ..measure.basis import Basis
    from ..spatial.location import Loc
    from ..temporal.period import Period


# class Balance:
#     def __init__(self, process: Process):
#         self.process = process

#         self.resource: Resource = None

#     @property
#     def network(self):
#         """Circumscribing Loc"""
#         return self.process.network

#     @property
#     def horizon(self):
#         """Circumscribing Period"""
#         return self.process.horizon

#     @property
#     def prg(self):
#         return self.process.prg

#     def __call__(self, resource: Resource):
#         self.resource = resource
#         return self

#     def __eq__(self, other: Conv):
#         setattr(
#             self.prg,
#             'produce',
#             V(
#                 self.resource.x,
#                 self.process.x,
#                 self.network.x,
#                 self.horizon.xset,
#                 mutable=True,
#             ),
#         )
#         exp = getattr(self.prg, 'produce')(
#             self.resource.x, self.process.x, self.network.x, self.horizon.xset
#         )
#         if not isinstance(other.res, list):
#             res_ = [other.res]
#             mul_ = [other.mul]
#         else:
#             res_ = other.res
#             mul_ = other.mul
#         for res, par in zip(res_, mul_):
#             if par > 0:
#                 setattr(
#                     self.prg,
#                     'produce',
#                     V(
#                         res.x,
#                         self.process.x,
#                         self.network.x,
#                         self.horizon.xset,
#                         mutable=True,
#                     ),
#                 )
#                 exp += par * getattr(self.prg, 'produce')(
#                     res.x, self.process.x, self.network.x, self.horizon.xset
#                 )
#             if par < 0:
#                 setattr(
#                     self.prg,
#                     'consume',
#                     V(
#                         res.x,
#                         self.process.x,
#                         self.network.x,
#                         self.horizon.xset,
#                         mutable=True,
#                     ),
#                 )
#                 exp -= -par * getattr(self.prg, 'consume')(
#                     res.x, self.process.x, self.network.x, self.horizon.xset
#                 )

#         setattr(self.prg, self.process.name + '_conv', exp == 0)


class Process(Task):
    """Process converts one Resource to another Resource"""

    def __init__(self, basis: Basis = None, label: str = None):
        Task.__init__(self, basis, label)
