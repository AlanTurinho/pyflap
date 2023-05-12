class State:
    def __init__(self, label: str = "", is_initial: bool = False, is_final: bool = False):
        self.label: str = label
        self.is_initial: bool = is_initial
        self.is_final: bool = is_final

        self.arrival_transactions: List[Transaction] = []
        self.departure_transactions: List[Transaction] = []

    def arrive(self, transaction):
        self.arrival_transactions.append(transaction)

    def departure(self, transaction):
        self.departure_transactions.append(transaction)

    def __str__(self):
        return self.label
