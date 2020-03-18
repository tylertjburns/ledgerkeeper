from ledgerkeeper.mongoData.ledger import LedgerItem
from ledgerkeeper.mongoData.account import Account
import datetime
from typing import List
from ledgerkeeper.enums import  TransactionSource, SpendCategory, TransactionTypes, PaymentType

from abc import ABC, abstractmethod

class ILedgerDataService(ABC):
    @abstractmethod
    def enter_if_not_exists(self,
            transaction_id: str,
            description: str,
            transaction_category: TransactionTypes,
            debit: float,
            credit: float,
            from_account: str,
            from_bucket: str,
            to_account: str,
            to_bucket: str,
            spend_category: SpendCategory,
            payment_type: PaymentType,
            source: TransactionSource,
            date_stamp: datetime.datetime = datetime.datetime.now,
            notes: str = "") -> LedgerItem:
      pass

    @abstractmethod
    def enter_ledger_entry(self,
                           transaction_id: str,
                           description: str,
                           transaction_category: TransactionTypes,
                           debit: float,
                           credit: float,
                           from_account: str,
                           from_bucket: str,
                           to_account: str,
                           to_bucket: str,
                           source: TransactionSource,
                           spend_category: SpendCategory,
                           payment_type: PaymentType,
                           date_stamp: datetime.datetime = datetime.datetime.now,
                           notes: str = "") -> LedgerItem:
        pass

    @abstractmethod
    def ledger_by_account(self,
                          account: str) -> List[LedgerItem]:
        pass

    @abstractmethod
    def find_ledger_by_description_date_debit_credit(self,
                                                     description: str
                                                     , date: datetime.date
                                                     , debit: float = 0
                                                     , credit: float = 0) -> LedgerItem:
        pass

    @abstractmethod
    def find_ledger_by_date_debit_credit(self,
                                         date: datetime.date, debit: float = 0, credit: float = 0) -> List[LedgerItem]:
       pass

    @abstractmethod
    def clear_ledger(self):
        pass

    @abstractmethod
    def query_ledger(self, query, raw_return=True, account_names: List[str] = None):
        pass

    @abstractmethod
    def delete_by_id(self, ledger_id: str):
        pass

    @abstractmethod
    def expense_history(self, start_date, end_date, account: Account = None):
        pass

    @abstractmethod
    def income_history(self, start_date, end_date):
        pass
