class Symbol:
    def __init__(self, label: str):
        self.label: str = label

    def __eq__(self, other):
        if not isinstance(other, Symbol):
            if isinstance(other, str):
                return self.label == other
            return NotImplemented
        return self.label == other.label

    def __str__(self):
        return self.label

    def __repr__(self):
        return self.label
