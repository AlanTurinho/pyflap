from src.automata import Automata

m = Automata(label="M1a", alphabet=['a', 'b', 'c'])

m.create_state(label="q0", is_initial=True, is_final=False)
m.create_state(label="q1", is_initial=False, is_final=True)
m.create_state(label="q2", is_initial=False, is_final=True)

m.create_transaction(departure_label="q0", arrival_label="q1", symbol="a")
m.create_transaction(departure_label="q1", arrival_label="q1", symbol="b")
m.create_transaction(departure_label="q1", arrival_label="q2", symbol="c")
m.create_transaction(departure_label="q2", arrival_label="q2", symbol="c")
m.create_transaction(departure_label="q2", arrival_label="q1", symbol="a")

print(m.tabular_notation)

# M1a.recognize(string="abbbccaccccabaaa")
