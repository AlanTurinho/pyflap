from typing import List, Dict, Union
from random import randint

import pandas as pd

from src.state import State
from src.transaction import Transaction


class Automata:
    def __init__(self, label: str, alphabet: List[str]):
        self.label: str = label
        self.is_total: bool = False

        self.sid: int = 0
        self.tid: int = 0

        self.states: Dict[int, State] = {}
        self.alphabet: List[str] = alphabet
        self.transactions: Dict[int, Transaction] = {}
        self.initial_state: State = None
        self.final_states: Dict[int, State] = {}

        self.tabular_notation: pd.DataFrame = self.update_tabular_notation()

    def update_tabular_notation(self) -> pd.DataFrame:

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
        for sid, state in self.states.items():
            if state.label == label:
                return sid
        return -1

    def create_state(self, label: str, is_initial: bool = False, is_final: bool = False):

        if self.check_state_existance(label=label) == -1:
            self.states[self.sid] = State(
                label=label,
                is_initial=is_initial,
                is_final=is_final
            )

            if is_initial:
                self.initial_state = self.states[self.sid]

            if is_final:
                self.final_states[self.sid] = self.states[self.sid]

            self.sid += 1

            self.tabular_notation = self.update_tabular_notation()


        else:
            raise ValueError(f"A state called {label} already exists.")

    def update_state(self, label: str, new_label: str = None, is_initial: bool = None, is_final: bool = None):
        sid: int = self.check_state_existance(label=label)

        self.states[sid].label = new_label if new_label else self.states[sid].label
        self.states[sid].is_initial = is_initial if is_initial else self.states[sid].is_initial
        self.states[sid].is_final = is_final if is_final else self.states[sid].is_final

        if sid >= 0:
            # update transactions
            for tid in self.transactions.keys():
                departure_label: str = self.transactions[tid].departure_state.label
                arrival_label: str = self.transactions[tid].arrival_state.label
                symbol: str = self.transactions[tid].symbol

                if departure_label == new_label:
                    self.transactions[tid].update_label()
                    self.update_transaction(
                        label=f"({departure_label},{symbol})->{arrival_label}",
                        new_departure_label=new_label
                    )

                if arrival_label == new_label:
                    self.transactions[tid].update_label()
                    self.update_transaction(
                        label=f"({departure_label},{symbol})->{arrival_label}",
                        new_arrival_label=new_label
                    )

            if is_initial is True:
                # the updated state becomes initial, regarless of the existence of one
                self.initial_state = self.states[sid]
            elif is_initial is False:
                if self.initial_state == self.states[sid]:
                    # if the updated state was initial and ceases to be
                    self.initial_state = None

            if is_final is True:
                # the updated state becomes final
                self.final_states[sid] = self.states[sid]
            elif is_final is False:
                if sid in self.final_states.keys():
                    # if the updated state was final and ceases to be
                    del self.final_states[sid]

            self.tabular_notation: pd.DataFrame = self.update_tabular_notation()
        else:
            raise ValueError(f"State {label} does not exist.")

    def delete_state(self, label: str):

        sid: int = self.check_state_existance(label=label)

        if sid >= 0:
            # if initial, remove initial
            if self.initial_state == self.states[sid]:
                self.initial_state = None

            # if final, remove final
            if sid in self.final_states.keys():
                del self.final_states[sid]

            # remove transactions
            t_labels_remove: List[int] = []
            for tid, transaction in self.transactions.items():
                if transaction.departure_state == self.states[sid] or transaction.arrival_state == self.states[sid]:
                    t_labels_remove.append(tid)

            for tid in t_labels_remove:
                departure_label: str = self.transactions[tid].departure_state.label
                arrival_label: str = self.transactions[tid].arrival_state.label
                symbol: str = self.transactions[tid].symbol
                self.delete_transaction(label=f"({departure_label},{symbol})->{arrival_label}")

            # delete state
            del self.states[sid]

            self.tabular_notation = self.update_tabular_notation()

        else:
            raise ValueError(f"State {label} does not exist.")

    def delete_states(self, labels: List[str]):

        for label in labels:
            self.delete_state(label=label)

    def check_transaction_existance(self, label: str) -> int:
        for tid, transaction in self.transactions.items():
            if transaction.label == label:
                return tid
        return -1

    def create_transaction(self, departure_label: str, arrival_label: str, symbol: str):

        t_label: str = f"({departure_label},{symbol})->{arrival_label}"

        if self.check_transaction_existance(label=t_label) == -1:
            departure_sid: int = self.check_state_existance(label=departure_label)
            arrival_sid: int = self.check_state_existance(label=arrival_label)
            if departure_sid >= 0:
                if arrival_sid >= 0:
                    if symbol in self.alphabet:
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

        tid: int = self.check_transaction_existance(label=label)

        if tid >= 0:
            departure_sid: int = self.check_state_existance(label=new_departure_label)
            arrival_sid: int = self.check_state_existance(label=new_arrival_label)

            if departure_sid >= 0:
                self.transactions[tid].departure_state = self.states[departure_sid] if new_departure_label else self.transactions[tid].departure_state

            if arrival_sid >= 0:
                self.transactions[tid].arrival_state = self.states[arrival_sid] if new_arrival_label else self.transactions[tid].arrival_state

            self.transactions[tid].symbol = new_symbol if new_symbol and new_symbol in self.alphabet else self.transactions[tid].symbol

            self.tabular_notation = self.update_tabular_notation()

        else:
            raise ValueError(f"The transaction {label} doesn't exist.")

    def delete_transaction(self, label: str):

        tid: int = self.check_transaction_existance(label=label)

        if tid >= 0:
            del self.transactions[tid]

            self.tabular_notation = self.update_tabular_notation()
        else:
            raise ValueError(f"The transaction {label} doesn't exist.")

    def delete_transactions(self, labels: List[str]):

        for label in labels:
            tid: int = self.check_transaction_existance(label=label)

            if tid >= 0:
                del self.transactions[tid]
            else:
                raise ValueError(f"The transaction {label} doesn't exist.")

    def recognize(self, string: str, verbose: bool = False) -> bool:

        def choose_transaction(sid: int, cursor: int) -> List[Transaction]:

            available_transactions: List[Transaction] = []

            for transaction in self.transactions.values():
                try:
                    if (transaction.departure_state.label == self.states[sid].label) and (transaction.symbol == string[cursor]):
                        available_transactions.append(transaction)
                except IndexError as e:
                    return []

            return available_transactions

        cursor: int = 0
        sid: int = self.check_state_existance(label=self.initial_state.label) if self.initial_state else None
        available_transactions: List[Transaction] = choose_transaction(sid=sid, cursor=cursor)

        if verbose:
            print(f"({self.states[sid].label},{string[cursor:]})", end=' -| ')

        while cursor <= len(string) and len(available_transactions) > 0:
            chosen_transaction = available_transactions[randint(0, len(available_transactions)-1)]

            cursor += 1
            sid = self.check_state_existance(label=chosen_transaction.arrival_state.label)
            available_transactions: List[Transaction] = choose_transaction(sid=sid, cursor=cursor)

            if verbose:
                print(f"({self.states[sid].label},{string[cursor:]})", end=' -| ')

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
