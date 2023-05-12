
class State:
    def __init__(self, label: str, is_initial: bool = False, is_final: bool = False):
        self.label: str = label
        self.is_initial: bool = is_initial
        self.is_final: bool = is_final

    def __str__(self):
        return self.label

    def __eq__(self, other):
        if not isinstance(other, State):
            return NotImplemented
        return self.label == other.label
