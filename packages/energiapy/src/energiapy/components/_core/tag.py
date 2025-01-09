"""Component"""


class Name:
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
        cls.__repr__ = Name.__repr__
        cls.__hash__ = Name.__hash__
