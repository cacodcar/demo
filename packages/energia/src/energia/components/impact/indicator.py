"""Impact Indicator"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ..core.modeling import Component

if TYPE_CHECKING:
    from ...modeling.impact import Impact


@dataclass
class Indicator(Component):
    """Impact Indicator"""

    def __post_init__(self):
        Component.__post_init__(self)
        # model sets this on the Impact collection object
        self.impact: Impact = None
