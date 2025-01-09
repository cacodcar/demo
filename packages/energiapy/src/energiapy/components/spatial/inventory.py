"""Inventory Space"""

from .._core.tag import Name


class Inv(Name):
    """Inventory space for Commodity"""

    def __init__(self, label='Inventory'):
        Name.__init__(self, label=label)


class InvPrc(Inv):
    """Inventory of commodity in Process"""

    def __init__(self):
        Inv.__init__(self, label='Inventory in process')


class InvStg(Inv):
    """Inventory of commodity in Storage"""

    def __init__(self):
        Inv.__init__(self, label='Inventory in storage')


class InvTrn(Inv):
    """Inventory of commodity in Transit"""

    def __init__(self):
        Inv.__init__(self, label='Inventory in transit')
