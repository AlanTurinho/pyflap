from src.automata import Automata

a = Automata(label="M", alphabet=['a', 'b', 'c', 'd', 'e'])

a.create_state(label="q0", is_initial=True, is_final=False)
a.create_state(label="q1", is_initial=False, is_final=True)
a.create_state(label="q2", is_initial=False, is_final=False)
a.create_state(label="q3", is_initial=False, is_final=True)
a.create_state(label="q4", is_initial=False, is_final=False)

a.create_transaction(departure_label="q0", arrival_label="q1", symbol="a")
a.create_transaction(departure_label="q0", arrival_label="q2", symbol="a")
a.create_transaction(departure_label="q1", arrival_label="q3", symbol="b")
a.create_transaction(departure_label="q1", arrival_label="q4", symbol="c")

print(a)
