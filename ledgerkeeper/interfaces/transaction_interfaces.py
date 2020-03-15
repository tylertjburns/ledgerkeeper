from abc import ABC, abstractmethod
from ledgerkeeper.enums import TransactionTypes, TransactionSource, PaymentType, TransactionStatus
from ledgerkeeper.mongoData.transaction import Transaction
import datetime

class ITransactionEnterer(ABC):
    @abstractmethod
    def enter_if_not_exists(self,
                            transaction_id: str,
                            description: str,
                            transaction_category: TransactionTypes,
                            debit: float,
                            credit: float,
                            source: TransactionSource,
                            payment_type: PaymentType,
                            date_stamp: datetime.datetime = datetime.datetime.now,
                            handled: TransactionStatus = TransactionStatus.UNHANDLED
                            ):
        pass

class ITransactionApprover(ABC):
    @abstractmethod
    def approve_transaction(self, transaction: Transaction):
        pass