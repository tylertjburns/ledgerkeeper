from ledgerkeeper.mongoData.transaction import Transaction
from ledgerkeeper.enums import TransactionStatus, TransactionTypes, TransactionSource, PaymentType
import datetime
from typing import List

from abc import ABC, abstractmethod

class ITransactionDataService(ABC):
    @abstractmethod
    def enter_if_not_exists(self, transaction_id: str,
        description: str,
        transaction_category: TransactionTypes,
        debit: float,
        credit: float,
        source: TransactionSource,
        payment_type: PaymentType,
        date_stamp: datetime.datetime = datetime.datetime.now,
        handled: TransactionStatus = TransactionStatus.UNHANDLED) -> Transaction:
        pass

    @abstractmethod
    def enter_transaction(self, transaction_id: str,
        description: str,
        transaction_category: TransactionTypes,
        debit: float,
        credit: float,
        source: TransactionSource,
        payment_type: PaymentType,
        date_stamp: datetime.datetime = datetime.datetime.now,
        handled:TransactionStatus = TransactionStatus.UNHANDLED) -> Transaction:
        pass

    @abstractmethod
    def query(self, query) -> List[Transaction]:
        pass

    @abstractmethod
    def clear_collection(self):
        pass

    @abstractmethod
    def unhandled_transactions(self) -> List[Transaction]:
        pass

    @abstractmethod
    def find_by_description_date_debit_credit(self, description: str, date: datetime.date, debit: float = 0,
                                                     credit: float = 0) -> List[Transaction]:
        pass

    @abstractmethod
    def mark_transaction_handled(self, transaction: Transaction, status=TransactionStatus.HANDLED) -> Transaction:
        pass



