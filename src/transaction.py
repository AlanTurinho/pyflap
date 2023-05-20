from src.state import State
from src.automata import Symbol


class Transaction:
    """Possibility of movement between two automata settings."""

    def __init__(self, departure_state: State, arrival_state: State, symbol: Symbol):
        self.departure_state: State = departure_state
        self.arrival_state: State = arrival_state
        self.symbol: Symbol = symbol
        self.label: str = f"({str(self.departure_state)},{self.symbol})->{str(self.arrival_state)}"
        self.loop: bool = True if departure_state == arrival_state else False

    def update_label(self):
        """Used whenever a state or a transaction are updated."""
        self.label: str = f"({str(self.departure_state)},{self.symbol})->{str(self.arrival_state)}"

    def __str__(self):
        return self.label

    def __eq__(self, other):
        if not isinstance(other, State):
            return NotImplemented
        return self.label == other.label


class MealyTransaction(Transaction):

    def __init__(self, departure_state: State, arrival_state: State, symbol: Symbol, output: Symbol):
        super().__init__(departure_state=departure_state, arrival_state=arrival_state, symbol=symbol)
        self.output: Symbol = output
        self.label: str = f"({str(self.departure_state)},{str(self.symbol)}/{str(self.output)})->{str(self.arrival_state)}"
