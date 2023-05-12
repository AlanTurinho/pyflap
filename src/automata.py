from typing import List, Literal

from state import State

class Automata:
    def __init__(self, label: str, alphabet: List[str]):
        self.id: str = label
        self.transaction_function_type: Literal["total", "partial"] = "partial"

        self.states: List[State] = []
        self.alphabet: List[str] = alphabet
        self.transactions: List[str] = []
        self.initial_state: State = None
        self.final_states: List[State] = []

    def check_existance(self, label: str) -> int:
        for i, s in enumerate(self.states):
            if s.label == label:
                return i
        return -1

    def create_state(self, state: State):

        if self.check_existance(label=state.label) == -1:
            self.states.append(state)

            if state.is_initial:
                self.initial_state = state

            if state.is_final:
                self.final_states.append(state)

        else:
            raise ValueError(f"Duplicated label, a state called {state.label} already exists.")

    def update_state(self, label: str, new_label: str = None, is_initial: bool = None, is_final: bool = None):

        i: int = self.check_existance(label=label)

        if i >= 0:
            self.states[i] = State(
                label=new_label if new_label else self.states[i].label,
                is_initial=is_initial if is_initial else self.states[i].is_initial,
                is_final=is_final if is_final else self.states[i].is_final,
            )

    def delete_state(self, label: str):

        i: int = self.check_existance(label=label)

        if i >= 0:
            del self.states[i]

    def delete_states(self, labels: List[str]):

        for label in labels:
            self.delete_state(label=label)

    def __str__(self):
        Q: str = f"{','.join([str(state) for state in self.states])}"
        S: str = f"{','.join([str(symbol) for symbol in self.alphabet])}"
        d: str = f""
        s0: str = str(self.initial_state)
        F: str = f"{','.join([str(state) for state in self.final_states])}"

        return f"""M = ({Q},{S},{d},{s0},{F})"""
