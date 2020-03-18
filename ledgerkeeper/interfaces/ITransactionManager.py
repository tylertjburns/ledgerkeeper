from ledgerkeeper.mongoData.transaction import Transaction
from abc import ABC, abstractmethod

class ITransactionManager(ABC):

    @abstractmethod
    def print_transactions(self):
        pass

    @abstractmethod
    def process_transaction_switch(self, input: int):
        pass

    @abstractmethod
    def process_transaction(self, transaction):
        pass

    @abstractmethod
    def process_transactions_loop(self):
        pass

    @abstractmethod
    def split_transaction(self, transaction: Transaction):
        pass

    @abstractmethod
    def deny_transaction(self, transaction):
        pass

    @abstractmethod
    def mark_transaction_duplicate(self, transaction):
        pass

    @abstractmethod
    def _enter_ledger_from_income_transaction(self, transaction:Transaction):
        pass

    @abstractmethod
    def _enter_ledger_from_expense_transaction(self, transaction:Transaction):
        pass

    @abstractmethod
    def approve_transaction(self, transaction):
        pass