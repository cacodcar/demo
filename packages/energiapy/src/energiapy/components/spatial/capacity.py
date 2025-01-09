"""Operating Space"""

from .._core.tag import Name


class Cap(Name):
    """Capacity space of operation"""

    def __init__(self, label='Capacity'):
        Name.__init__(self, label=label)


class CapPrc(Cap):
    """Capacity of Process"""

    def __init__(self):
        Cap.__init__(self, label='Capacity of process')


class CapStg(Cap):
    """Capacity of Storage"""

    def __init__(self):
        Cap.__init__(self, label='Capacity of storage')


class CapTrn(Cap):
    """Capacity of Transit"""

    def __init__(self):
        Cap.__init__(self, label='Capacity of transit')
