
class State:
    """
    Labeled element responsible for recording information gathered in the past, but also relevant for future decisions.
    """

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


class MooreState(State):

    def __init__(self, label: str, is_initial: bool = False, is_final: bool = False):
        super().__init__(label=label, is_initial=is_initial, is_final=is_final)
        pass
