from typing import List

from src.symbol import Symbol

class Alphabet:
    def __init__(self, symbol_labels: List[str]):
        self.symbols: List[Symbol] = [Symbol(symbol) for symbol in symbol_labels]

    def __eq__(self, other):
        if not isinstance(other, Alphabet):
            return NotImplemented
        return self.symbols == other.symbols

    def __str__(self):
        return str(self.symbols)

    def __len__(self):
        return len(self.symbols)

    def __getitem__(self, item):
        return self.symbols[item]

    def __repr__(self):
        return str(self.symbols)

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < len(self.symbols):
            symbol: Symbol = self.symbols[self.n]
            self.n += 1
            return symbol
        else:
            raise StopIteration

