from src.state import State


class Transaction:
    def __init__(self, departure_state: State, arrival_state: State, symbol: str):
        self.departure_state: State = departure_state
        self.arrival_state: State = arrival_state
        self.symbol: str = symbol
        self.label: str = f"({str(self.departure_state)},{self.symbol})->{str(self.arrival_state)}"
        self.loop: bool = True if departure_state == arrival_state else False

    def __str__(self):
        return self.label

    def __eq__(self, other):
        if not isinstance(other, State):
            return NotImplemented
        return self.label == other.label