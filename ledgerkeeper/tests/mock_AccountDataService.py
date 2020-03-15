from mongoData.account import Account
from mongoData.bucket import Bucket
from mongoData.openBalance import OpenBalance

from ledgerkeeper.interfaces.IAccountDataService import IAccountDataService
from ledgerkeeper.enums import AccountType, SpendCategory
from typing import List, Dict

class mock_AccountDataService(IAccountDataService):

    def enter_account(self, name: str, description: str, type: AccountType) -> Account:
        return Account()

    def delete_account(self, name: str):
        return Account()

    def inactivate_account(self, account: Account) -> Account:
        return Account()

    def add_bucket_to_account(self, account: Account, name: str, priority: int, due_day_of_month: int,
                              spend_category: SpendCategory, base_budget_amount: float = 0.0,
                              perc_budget_amount: float = 0.0, waterfall_amount: float = 0.0, saved_amount: float = 0.0,
                              percent_of_income_adjustment_amount: float = 0.0) -> Bucket:
        return Bucket()

    def update_bucket(self, account: Account, bucketName: str, priority: int = None, due_day_of_month: int = None,
                      spend_category: SpendCategory = None, base_budget_amount: float = None,
                      perc_budget_amount: float = None, waterfall_amount: float = None, saved_amount: float = None,
                      percent_of_income_adjustment_amount: float = None) -> Bucket:
        return Bucket()

    def bucket_by_account_and_name(self, account: Account, bucketName: str) -> Bucket:
        return Bucket()

    def account_by_name(self, account_name: str) -> Account:
        return Account()

    def accounts_as_dict(self, statusList: List[str] = None) -> Dict[int, str]:
        return {1: "test"}

    def query_account(self, query, accountNames: List[str] = None) -> List[Account]:
        l = []
        l.append(Account())
        return l

    def buckets_by_account(self, account: Account, raw_return=False) -> List[Bucket]:
        l = []
        l.append(Bucket())
        return l

    def buckets_as_dict_by_account(self, account: Account, exceptedValues=None) -> Dict[int, str]:
        return {1: "test"}

    def bucket_by_name(self, account: Account, bucket_name: str) -> Bucket:
        return Bucket()

    def spend_category_by_bucket_name(self, account: Account, bucket_name) -> str:
        return "testName"

    def delete_bucket_from_account(self, account, bucketName):
        return Bucket()

    def add_open_balance_to_account(self, account: Account, balanceName: str, balanceValue: float):
        return OpenBalance()

    def balance_by_name_and_account(self, account: Account, balanceName: str):
        return OpenBalance()

    def delete_open_balance_from_account(self, account: Account, balanceName: str):
        return OpenBalance()

    def balances_as_dict_by_account(self, account: Account, exceptedValues=None):
        return {1: "testBalance"}

    def balances_by_account(self, account: Account, raw_return=False) -> List[OpenBalance]:
        l = []
        l.append(OpenBalance())
        return l

    def enter_account_if_not_exists(self, name: str, description: str, type: AccountType) -> Account:
        return Account()
