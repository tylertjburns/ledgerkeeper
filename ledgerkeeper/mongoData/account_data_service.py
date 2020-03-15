import datetime

from ledgerkeeper.mongoData.account import Account
from ledgerkeeper.mongoData.bucket import Bucket
from ledgerkeeper.mongoData.openBalance import OpenBalance
from ledgerkeeper.enums import SpendCategory, AccountStatus, AccountType
from typing import List, Dict

from ledgerkeeper.interfaces.IAccountDataService import IAccountDataService

class AccountDataservice(IAccountDataService):

    def enter_account_if_not_exists(self,
                                    name: str,
                                    description: str,
                                    type: AccountType) -> Account:

        existing = Account.objects(account_name=name)

        if len(existing) > 0:
            return None
        else:
            return self.enter_account(name
                                      , description
                                      , type
                                     )

    def delete_account(self,
                                    name:str):
        account = self.account_by_name(name)

        account.delete()

    def enter_account(self,
                      name: str,
                      description: str,
                      type: AccountType
        ) -> Account:

        account = Account()
        account.account_name = name
        account.description = description
        account.type = type.name
        account.status = AccountStatus.ACTIVE.name

        account.save()

        return account

    def inactivate_account(self,account: Account):
        account.status = AccountStatus.INACTIVE.name

        account.save()

        return account

    def add_bucket_to_account(self,account: Account,
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
        bucket = Bucket()
        bucket.name = name
        bucket.priority = priority
        bucket.due_day_of_month = due_day_of_month
        bucket.spend_category = spend_category.name
        bucket.base_budget_amount = base_budget_amount
        bucket.perc_budget_amount = perc_budget_amount
        bucket.waterfall_amount = waterfall_amount
        bucket.saved_amount = saved_amount
        bucket.percent_of_income_adjustment_amount = percent_of_income_adjustment_amount

        account = Account.objects(id=account.id).first()
        account.buckets.append(bucket)
        account.save()

        return bucket

    def update_bucket(self,account: Account, bucketName: str,
                      priority: int = None,
                      due_day_of_month: int = None,
                      spend_category: SpendCategory = None,
                      base_budget_amount: float = None,
                      perc_budget_amount: float = None,
                      waterfall_amount: float = None,
                      saved_amount: float = None,
                      percent_of_income_adjustment_amount: float = None,
                      ):

        bucket = self.bucket_by_account_and_name(account, bucketName)

        bucket.update(
            priority = priority if priority else bucket.priority,
            due_day_of_month = due_day_of_month if due_day_of_month else bucket.due_day_of_month,
            spend_category = spend_category.name if spend_category else bucket.spend_category,
            base_budget_amount = base_budget_amount if base_budget_amount else bucket.base_budget_amount,
            perc_budget_amount = perc_budget_amount if perc_budget_amount else bucket.perc_budget_amount,
            waterfall_amount = waterfall_amount if waterfall_amount else bucket.waterfall_amount,
            saved_amount = saved_amount if saved_amount else bucket.saved_amount,
            percent_of_income_adjustment_amount = percent_of_income_adjustment_amount if percent_of_income_adjustment_amount else bucket.percent_of_income_adjustment_amount
        )
        bucket.reload()

        account.save()

        return bucket

    def bucket_by_account_and_name(self,account: Account
                                   , bucketName: str):
        # bucket = account.buckets.objects(name=bucketName).get()
        bucket = [bucket for bucket in account.buckets if bucket.name == bucketName][0]
        return bucket

    def update_bucket_saved_amount(self,account: Account
                             , bucketName: str
                             , newAmount: float):
        bucket = self.bucket_by_account_and_name(account, bucketName)
        bucket.saved_amount = round(newAmount, 2)

        account.save()

        return bucket

    def update_bucket_waterfall_amount(self,account: Account
                             , bucketName: str
                             , newAmount: float):
        bucket = self.bucket_by_account_and_name(account, bucketName)
        bucket.waterfall_amount = round(newAmount, 2)
        account.save()

        return bucket

    def update_bucket_base_budget_amount(self,account: Account
                                    , bucketName:str
                                    , newAmount: float):
        bucket = self.bucket_by_account_and_name(account, bucketName)
        bucket.base_budget_amount = round(newAmount, 2)
        account.save()

        return bucket

    def update_bucket_percentage_amount(self,account: Account
                                    , bucketName:str
                                    , newPerc: float):
        bucket = self.bucket_by_account_and_name(account, bucketName)
        bucket.percent_of_income_adjustment_amount = round(newPerc, 2)
        account.save()

        return bucket

    def update_bucket_percentage_budget_amount(self,account: Account
                                    , bucketName:str
                                    , newAmount: float):
        bucket = self.bucket_by_account_and_name(account, bucketName)
        bucket.perc_budget_amount = round(newAmount, 2)
        account.save()

        return bucket

    def update_bucket_priority(self,account: Account,
                               bucketName: str,
                               newPriority: int):
        bucket = self.bucket_by_account_and_name(account, bucketName)
        bucket.priority = newPriority
        account.save()

        return bucket



    def account_by_name(self,account_name: str) -> Account:
        return Account.objects(account_name=account_name).first()

    def accounts_as_dict(self,statusList:List[str] = None) -> Dict[int, str]:
        accounts = self.query_account('')
        if statusList is None:
            return {i + 1: accounts[i].account_name for i in range(0, len(accounts))}
        else:
            return {i + 1: accounts[i].account_name for i in range(0, len(accounts)) if accounts[i].status in statusList}

    def query_account(self,query, accountNames: List[str] = None) -> List[Account]:

        if accountNames is None:
            accounts = Account.objects()
        else:
            accounts = Account.objects().filter(account_name__in=accountNames)

        if query == "":
            return accounts.order_by('date_stamp')
        else:
            return accounts.filter(__raw__=query).order_by('date_stamp')

    def buckets_by_account(self,account:Account, raw_return = False) -> List[Bucket]:

        buckets = Account.objects(id=account.id).first().buckets

        if raw_return:
            return buckets.as_pymongo()
        else:
            bucket_list =[
                bucket for bucket in buckets
            ]

            return bucket_list

        # return Account.objects(id=account.id).first().buckets.filter()

    def buckets_as_dict_by_account(self,account: Account, exceptedValues=None) -> Dict[int, str]:
        if exceptedValues is None:
            exceptedValues = set()

        buckets = self.buckets_by_account(account)
        buckets = [bucket for bucket in buckets if bucket.name not in exceptedValues]
        return {i + 1: buckets[i].name for i in range(0, len(buckets))}

    def bucket_by_name(self,account:Account, bucket_name: str) -> Bucket:
        return Bucket.objects()\
            .filter(name=bucket_name)\
            .filter(account__name=account.name).first()

    def spend_category_by_bucket_name(self,account:Account, bucket_name) -> str:
        return self.bucket_by_account_and_name(account=account, bucketName=bucket_name).spend_category
        # return bucket_by_name(account, bucket_name).spend_category


    def delete_bucket_from_account(self,account, bucketName):
        bucket = self.bucket_by_name(account, bucketName)
        bucket.delete()

    def add_open_balance_to_account(self,account:Account, balanceName: str, balanceValue: float):
        balance = OpenBalance()
        balance.name = balanceName
        balance.amount = balanceValue
        balance.entry_date = datetime.datetime.now()

        account.openBalances.append(balance)

        account.save()
        return balance

    def balance_by_name_and_account(self,account:Account, balanceName: str):
        return OpenBalance.objects() \
            .filter(name=balanceName) \
            .filter(account__name=account.name).first()

    def delete_open_balance_from_account(self,account:Account, balanceName: str):
        balance = self.balance_by_name_and_account(account, balanceName)
        balance.delete()

    def balances_as_dict_by_account(self,account: Account, exceptedValues=None):
        if exceptedValues is None:
            exceptedValues = set()

        balances = self.balances_by_account(account)
        balances = [balance for balance in balances if balance.name not in exceptedValues]
        return {i + 1: balances[i].name for i in range(0, len(balances))}

    def balances_by_account(self,account:Account, raw_return=False) -> List[OpenBalance]:

        balances = Account.objects(id=account.id).first().openBalances

        if raw_return:
            return balances.as_pymongo()
        else:
            balance_list =[
                balance for balance in balances
            ]

            return balance_list

