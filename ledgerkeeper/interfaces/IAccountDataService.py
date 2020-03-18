from ledgerkeeper.mongoData.account import Account
from ledgerkeeper.mongoData.bucket import Bucket
from ledgerkeeper.mongoData.openBalance import OpenBalance
from ledgerkeeper.enums import SpendCategory, AccountType
from typing import List, Dict

from abc import ABC, abstractmethod

class IAccountDataService(ABC):
    @abstractmethod
    def enter_account_if_not_exists(self, name: str,
                                    description: str,
                                    type: AccountType) -> Account:
        pass

    @abstractmethod
    def enter_account(self, name: str,
        description: str,
        type: AccountType
        ) -> Account:
        pass

    @abstractmethod
    def delete_account(self, name:str):
        pass

    @abstractmethod
    def inactivate_account(self, account: Account) -> Account:
        pass

    @abstractmethod
    def add_bucket_to_account(self,
                              account: Account,
                              name: str,
                              priority: int,
                              due_day_of_month: int,
                              spend_category: SpendCategory,
                              base_budget_amount: float = 0.0,
                              perc_budget_amount: float = 0.0,
                              waterfall_amount: float = 0.0,
                              saved_amount: float = 0.0,
                              percent_of_income_adjustment_amount:float = 0.0,
                              ) -> Bucket:
        pass

    @abstractmethod
    def update_bucket(self,
                      account: Account, bucketName: str,
                      priority: int = None,
                      due_day_of_month: int = None,
                      spend_category: SpendCategory = None,
                      base_budget_amount: float = None,
                      perc_budget_amount: float = None,
                      waterfall_amount: float = None,
                      saved_amount: float = None,
                      percent_of_income_adjustment_amount: float = None,
                      ) -> Bucket:
        pass

    @abstractmethod
    def bucket_by_account_and_name(self, account: Account
                                   , bucketName: str) -> Bucket:
        pass

    @abstractmethod
    def account_by_name(self, account_name: str) -> Account:
        pass

    @abstractmethod
    def accounts_as_dict(self, statusList:List[str] = None) -> Dict[int, str]:
        pass

    @abstractmethod
    def query_account(self, query, accountNames: List[str] = None) -> List[Account]:
        pass
    @abstractmethod
    def buckets_by_account(self, account:Account, raw_return = False) -> List[Bucket]:
        pass

    @abstractmethod
    def buckets_as_dict_by_account(self, account: Account, exceptedValues=None) -> Dict[int, str]:
        pass
    @abstractmethod
    def bucket_by_name(self, account:Account, bucket_name: str) -> Bucket:
        pass
    @abstractmethod
    def spend_category_by_bucket_name(self, account:Account, bucket_name) -> str:
        pass
    @abstractmethod
    def delete_bucket_from_account(self, account, bucketName):
        pass
    @abstractmethod
    def add_open_balance_to_account(self, account:Account, balanceName: str, balanceValue: float):
        pass
    @abstractmethod
    def balance_by_name_and_account(self, account:Account, balanceName: str):
        pass
    @abstractmethod
    def delete_open_balance_from_account(self, account:Account, balanceName: str):
        pass
    @abstractmethod
    def balances_as_dict_by_account(self, account: Account, exceptedValues=None):
        pass
    @abstractmethod
    def balances_by_account(self, account:Account, raw_return=False) -> List[OpenBalance]:
        pass