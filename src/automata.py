from typing import List

from src.state import State
from src.transaction import Transaction


class Automata:
    def __init__(self, label: str, alphabet: List[str]):
        self.label: str = label
        self.is_total: bool = False

        self.states: List[State] = []
        self.alphabet: List[str] = alphabet
        self.transactions: List[Transaction] = []
        self.initial_state: State = None
        self.final_states: List[State] = []

    def check_state_existance(self, label: str) -> int:
        for i, s in enumerate(self.states):
            if s.label == label:
                return i
        return -1

    def create_state(self, label: str, is_initial: bool = False, is_final: bool = False):

        if self.check_state_existance(label=label) == -1:

            self.states.append(
                State(
                    label=label,
                    is_initial=is_initial,
                    is_final=is_final
                )
            )

            if is_initial:
                self.initial_state = self.states[-1]

            if is_final:
                self.final_states.append(self.states[-1])

        else:
            raise ValueError(f"A state called {label} already exists.")

    def update_state(self, label: str, new_label: str = None, is_initial: bool = None, is_final: bool = None):

        i: int = self.check_state_existance(label=label)

        if i >= 0:
            self.states[i].label = new_label if new_label else self.states[i].label
            self.states[i].is_initial = is_initial if is_initial else self.states[i].is_initial
            self.states[i].is_final = is_final if is_final else self.states[i].is_final

            if is_initial:
                # the updated state becomes initial, regarless of the existence of one
                self.initial_state = self.states[i]
            else:
                if self.initial_state == self.states[i]:
                    # if the updated state was initial and ceases to be
                    self.initial_state = None
        else:
            raise ValueError(f"State {label} does not exist.")

    def delete_state(self, label: str):

        i: int = self.check_state_existance(label=label)

        if i >= 0:
            if self.initial_state == self.states[i]:
                self.initial_state = None

            if self.states[i] in self.final_states:
                self.final_states.remove(self.states[i])

            it_to_remove: List[int] = []
            for it, t in enumerate(self.transactions):
                if t.departure_state == self.states[i] or t.arrival_state == self.states[i]:
                    it_to_remove.append(it)

            for it in it_to_remove:
                departure_label: str = self.transactions[it].departure_state.label
                arrival_label: str = self.transactions[it].arrival_state.label
                symbol: str = self.transactions[it].symbol
                self.delete_transaction(departure_label=departure_label, arrival_label=arrival_label, symbol=symbol)

            del self.states[i]

        else:
            raise ValueError(f"State {label} does not exist.")

    def delete_states(self, labels: List[str]):

        for label in labels:
            self.delete_state(label=label)

    def check_transaction_existance(self, label: str) -> int:

        for i, t in enumerate(self.transactions):
            if t.label == label:
                return i
        return -1

    def create_transaction(self, departure_label: str, arrival_label: str, symbol):

        if self.check_transaction_existance(label=f"({departure_label},{symbol})->{arrival_label}") == -1:

            i_departure: int = self.check_state_existance(label=departure_label)
            i_arrival: int = self.check_state_existance(label=arrival_label)

            if i_departure >= 0:
                if i_arrival >= 0:
                    if symbol in self.alphabet:
                        self.transactions.append(
                            Transaction(
                                departure_state=self.states[i_departure],
                                arrival_state=self.states[i_arrival],
                                symbol=symbol
                            )
                        )
                    else:
                        raise ValueError(f"Symbol {symbol} does not exist in alphabet.")
                else:
                    raise ValueError(f"State {arrival_label} does not exist in list of states.")
            else:
                raise ValueError(f"State {departure_label} does not exist in list of states.")
        else:
            raise ValueError(f"A transaction from {departure_label} to {arrival_label} consuming {symbol} already exists.")

    def update_transaction(
            self, departure_label: str, arrival_label: str, symbol: str,
            new_label_departure: str, new_label_arrival, new_symbol: str
    ):

        i: int = self.check_transaction_existance(label=f"({departure_label},{symbol})->{arrival_label}")

        if i >= 0:
            i_departure: int = self.check_state_existance(label=new_label_departure)
            i_arrival: int = self.check_state_existance(label=new_label_arrival)

            self.transactions[i].departure_state = self.states[i_departure] if new_label_departure else self.transactions[i].departure_state
            self.transactions[i].arrival_state = self.states[i_arrival] if new_label_arrival else self.transactions[i].arrival_state,
            self.transactions[i].symbol = new_symbol if new_symbol else self.transactions[i].symbol,

    def delete_transaction(self, departure_label: str, arrival_label: str, symbol: str,):

        i: int = self.check_transaction_existance(label=f"({departure_label},{symbol})->{arrival_label}")

        if i >= 0:
            del self.transactions[i]

    def __str__(self):
        Q: str = ', '.join([str(state) for state in self.states])
        S: str = ', '.join([str(symbol) for symbol in self.alphabet])
        d: str = ', '.join([str(transaction) for transaction in self.transactions])
        s0: str = str(self.initial_state)
        F: str = ', '.join([str(state) for state in self.final_states])

        return f"""{self.label} = (\n\t{{{Q}}},\n\t{{{S}}},\n\t{{{d}}},\n\t{s0},\n\t{{{F}}}\n)"""
