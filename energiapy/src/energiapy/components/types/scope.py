"""ScpCmp"""

from .defined import DefCmp


class ScpCmp(DefCmp):
    """Defines the scope of the problem"""

    def __init__(self, label=None):

        DefCmp.__init__(self, label)
