from typing import List, Dict, Union
from random import randint

import pandas as pd

from src.state import State
from src.transaction import Transaction


class Automata:
    """Entities composed of states and transitions, used to accept or to reject a sentence."""

    def __init__(self, label: str, alphabet: List[str]):
        self.label: str = label

        # quintuple of elements that define an automata
        self.states: Dict[int, State] = {}
        self.alphabet: List[str] = alphabet
        self.transactions: Dict[int, Transaction] = {}
        self.initial_state: State = None
        self.final_states: Dict[int, State] = {}

        self.sid: int = 0  # state id
        self.tid: int = 0  # transaction id

        self.is_total: bool = False

        self.tabular_notation: pd.DataFrame = self.update_tabular_notation()

    def update_tabular_notation(self) -> pd.DataFrame:
        """Dataframe that describes general information for all states."""

        data: Dict[str, List[Union[str, bool, List[str]]]] = {
            "sid": [sid for sid in self.states.keys()],
            "initial": [state.is_initial for state in self.states.values()],
            "final": [state.is_final for state in self.states.values()],
            "state": [state.label for state in self.states.values()],
        }

        for symbol in self.alphabet:
            symbol_transactions: Dict[str, List[str]] = {state: [] for state in data["state"]}
            for transaction in self.transactions.values():
                if transaction.symbol == symbol:
                    symbol_transactions[transaction.departure_state.label].append(transaction.arrival_state.label)
            data[symbol] = [arrival_states for arrival_states in symbol_transactions.values()]

        return pd.DataFrame(data=data)

    def check_state_existance(self, label: str) -> int:
        """If a given label exists in the dictionary of states, return its sid."""

        for sid, state in self.states.items():
            if state.label == label:
                return sid
        return -1

    def create_state(self, label: str, is_initial: bool = False, is_final: bool = False):
        """Create state and update quintuple."""

        # if given label don't exist
        if self.check_state_existance(label=label) == -1:
            # create state and store at current sid position
            self.states[self.sid] = State(
                label=label,
                is_initial=is_initial,
                is_final=is_final
            )

            if is_initial:
                self.initial_state = self.states[self.sid]  # if initial, it becomes the only initial

            if is_final:
                self.final_states[self.sid] = self.states[self.sid]  # if final, add to the dictionary of final states

            self.sid += 1

            self.tabular_notation = self.update_tabular_notation()
        else:
            raise ValueError(f"A state called {label} already exists.")

    def update_state(self, label: str, new_label: str = None, is_initial: bool = None, is_final: bool = None):
        """Update state information and all transactions associated."""

        # store sid
        sid: int = self.check_state_existance(label=label)

        if sid >= 0:
            # update state information
            self.states[sid].label = new_label if new_label else self.states[sid].label
            self.states[sid].is_initial = is_initial if is_initial else self.states[sid].is_initial
            self.states[sid].is_final = is_final if is_final else self.states[sid].is_final

            # update transactions
            for tid in self.transactions.keys():
                departure_label: str = self.transactions[tid].departure_state.label
                arrival_label: str = self.transactions[tid].arrival_state.label
                symbol: str = self.transactions[tid].symbol

                # if the updated state is a departure, update label
                if departure_label == new_label:
                    self.transactions[tid].update_label()
                    self.update_transaction(
                        label=f"({departure_label},{symbol})->{arrival_label}",
                        new_departure_label=new_label
                    )

                # if the updated state is a arrival, update label
                if arrival_label == new_label:
                    self.transactions[tid].update_label()
                    self.update_transaction(
                        label=f"({departure_label},{symbol})->{arrival_label}",
                        new_arrival_label=new_label
                    )

            if is_initial is True:
                self.initial_state = self.states[sid]  # if initial, it becomes the only initial
            elif is_initial is False:
                if self.initial_state == self.states[sid]:
                    self.initial_state = None  # if the updated state was initial and ceases to be, no one is initial

            if is_final is True:
                self.final_states[sid] = self.states[sid]  # the updated state becomes final
            elif is_final is False:
                if sid in self.final_states.keys():
                    del self.final_states[sid]  # if the updated state was final and ceases to be, delete it

            self.tabular_notation: pd.DataFrame = self.update_tabular_notation()
        else:
            raise ValueError(f"State {label} does not exist.")

    def delete_state(self, label: str):
        """Delete state and update quintuple."""

        # store sid
        sid: int = self.check_state_existance(label=label)

        if sid >= 0:
            if self.initial_state == self.states[sid]:
                self.initial_state = None  # if the deleted state is initial, no one is initial

            if sid in self.final_states.keys():
                del self.final_states[sid]  # if the deleted state is final, delete it

            # to remove its transactions, first collect tids of transactions that use this state
            tids_to_remove: List[int] = []
            for tid, transaction in self.transactions.items():
                if transaction.departure_state == self.states[sid] or transaction.arrival_state == self.states[sid]:
                    tids_to_remove.append(tid)

            # then delete all transactions of this state
            for tid in tids_to_remove:
                departure_label: str = self.transactions[tid].departure_state.label
                arrival_label: str = self.transactions[tid].arrival_state.label
                symbol: str = self.transactions[tid].symbol
                self.delete_transaction(label=f"({departure_label},{symbol})->{arrival_label}")

            del self.states[sid]  # delete state

            self.tabular_notation = self.update_tabular_notation()

        else:
            raise ValueError(f"State {label} does not exist.")

    def delete_states(self, labels: List[str]):
        """Delete a list of states and update quintuple."""

        for label in labels:
            self.delete_state(label=label)

    def check_transaction_existance(self, label: str) -> int:
        """If a given label exists in the dictionary of transactions, return its tid."""

        for tid, transaction in self.transactions.items():
            if transaction.label == label:
                return tid
        return -1

    def create_transaction(self, departure_label: str, arrival_label: str, symbol: str):
        """Create transaction and update quintuple"""

        # transaction label indicates a transaction function from qi to qj consuming s: (qi,s)->qj
        t_label: str = f"({departure_label},{symbol})->{arrival_label}"

        # if the label don't exist
        if self.check_transaction_existance(label=t_label) == -1:
            departure_sid: int = self.check_state_existance(label=departure_label)
            arrival_sid: int = self.check_state_existance(label=arrival_label)

            if departure_sid >= 0:
                if arrival_sid >= 0:
                    if symbol in self.alphabet:
                        # if the departure and arrival exist and the alphabet contains the alphabet,
                        # create transaction and store at current tid position
                        self.transactions[self.tid] = Transaction(
                            departure_state=self.states[departure_sid],
                            arrival_state=self.states[arrival_sid],
                            symbol=symbol
                        )
                        self.tid += 1

                        self.tabular_notation = self.update_tabular_notation()
                    else:
                        raise ValueError(f"Symbol {symbol} does not exist in alphabet.")
                else:
                    raise ValueError(f"State {arrival_label} does not exist in list of states.")
            else:
                raise ValueError(f"State {departure_label} does not exist in list of states.")
        else:
            raise ValueError(f"A transaction from {departure_label} to {arrival_label} consuming {symbol} already exists.")

    def update_transaction(
            self, label: str, new_departure_label: str = None, new_arrival_label: str = None, new_symbol: str = None
    ):
        """Update transaction information."""

        # store tid
        tid: int = self.check_transaction_existance(label=label)

        if tid >= 0:
            # update transaction information
            departure_sid: int = self.check_state_existance(label=new_departure_label)
            arrival_sid: int = self.check_state_existance(label=new_arrival_label)

            # update departure label, if provided
            if departure_sid >= 0:
                if new_departure_label:
                    self.transactions[tid].departure_state = self.states[departure_sid]

            # update arrival label, if provided
            if arrival_sid >= 0:
                if new_arrival_label:
                    self.transactions[tid].arrival_state = self.states[arrival_sid]

            # update symbol, if provided
            if new_symbol in self.alphabet:
                self.transactions[tid].symbol = new_symbol

            self.tabular_notation = self.update_tabular_notation()
        else:
            raise ValueError(f"The transaction {label} doesn't exist.")

    def delete_transaction(self, label: str):
        """Delete transaction and update quintuple."""

        # store tid
        tid: int = self.check_transaction_existance(label=label)

        if tid >= 0:
            del self.transactions[tid]  # delete transaction

            self.tabular_notation = self.update_tabular_notation()
        else:
            raise ValueError(f"The transaction {label} doesn't exist.")

    def delete_transactions(self, labels: List[str]):
        """Delete a list of transactions and update quintuple."""

        for label in labels:
            self.delete_transaction(label=label)

    def recognize(self, string: str, verbose: bool = False) -> bool:
        """Process a string of symbols and return a boolean to indicate acception and rejection."""

        def get_transactions(current_sid: int, current_cursor: int) -> List[Transaction]:
            """List all available transactions from current state."""

            current_available_transactions: List[Transaction] = []

            for transaction in self.transactions.values():
                try:
                    if transaction.departure_state.label == self.states[current_sid].label:
                        if transaction.symbol == string[current_cursor]:
                            current_available_transactions.append(transaction)
                except IndexError as e:
                    return []

            return current_available_transactions

        # declare initial setting
        cursor: int = 0
        sid: int = self.check_state_existance(label=self.initial_state.label) if self.initial_state else None
        available_transactions: List[Transaction] = get_transactions(current_sid=sid, current_cursor=cursor)

        if verbose:
            print(f"({self.states[sid].label},{string[cursor:]})", end=' -| ')

        # while the string has symbols left and there is available transactions
        while cursor <= len(string) and len(available_transactions) > 0:

            # choose a transaction from the list of chosen transactions
            chosen_id: int = randint(0, len(available_transactions)-1)
            chosen_transaction = available_transactions[chosen_id]

            cursor += 1  # move the cursor

            # move to the sid indicated by the chosen transaction
            sid = self.check_state_existance(label=chosen_transaction.arrival_state.label)

            # update the list of available transactions of the chosen state
            available_transactions: List[Transaction] = get_transactions(current_sid=sid, current_cursor=cursor)

            if verbose:
                print(f"({self.states[sid].label},{string[cursor:]})", end=' -| ')

        # if it reached a final state and there is no more symbols to consume, then accept, otherwise reject
        if self.states[sid].is_final and cursor >= len(string):
            if verbose:
                print(f"({self.states[sid].label},{None})")
            return True
        return False

    def __str__(self):
        Q: str = ', '.join([str(state) for state in self.states.values()])
        S: str = ', '.join([str(symbol) for symbol in self.alphabet])
        d: str = ', '.join([str(transaction) for transaction in self.transactions.values()])
        s0: str = str(self.initial_state)
        F: str = ', '.join([str(state) for state in self.final_states.values()])

        return f"""{self.label} = (\n\t{{{Q}}},\n\t{{{S}}},\n\t{{{d}}},\n\t{s0},\n\t{{{F}}}\n)"""
