from ledgerkeeper.mongoData.account import Account
from ledgerkeeper.mongoData.bucket import Bucket
from ledgerkeeper.enums import SpendCategory
from typing import List, Dict

def enter_if_not_exists(name: str,
    description: str,
    type: str) -> Account:

    existing = Account.objects(account_name=name)

    if len(existing) > 0:
        return None
    else:
        return enter_transaction(name
                                  , description
                                  , type
                                 )

def delete_account(name:str):
    account = account_by_name(name)

    account.delete()

def enter_transaction(name: str,
    description: str,
    type: str
    ) -> Account:

    account = Account()
    account.account_name = name
    account.description = description
    account.type = type

    account.save()

    return account

def add_bucket_to_account(account: Account,
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

def bucket_by_account_and_name(account: Account
                               , bucketName: str):
    bucket = [bucket for bucket in account.buckets if bucket.name == bucketName][0]
    return bucket

def update_bucket_saved_amount(account: Account
                         , bucketName: str
                         , newAmount: float):
    bucket = bucket_by_account_and_name(account, bucketName)
    bucket.saved_amount = round(newAmount, 2)

    account.save()

    return bucket

def update_bucket_waterfall_amount(account: Account
                         , bucketName: str
                         , newAmount: float):
    bucket = bucket_by_account_and_name(account, bucketName)
    bucket.waterfall_amount = round(newAmount, 2)
    account.save()

    return bucket

def update_bucket_base_budget_amount(account: Account
                                , bucketName:str
                                , newAmount: float):
    bucket = bucket_by_account_and_name(account, bucketName)
    bucket.base_budget_amount = round(newAmount, 2)
    account.save()

    return bucket

def update_bucket_percentage_amount(account: Account
                                , bucketName:str
                                , newPerc: float):
    bucket = bucket_by_account_and_name(account, bucketName)
    bucket.percent_of_income_adjustment_amount = round(newPerc, 2)
    account.save()

    return bucket

def update_bucket_percentage_budget_amount(account: Account
                                , bucketName:str
                                , newAmount: float):
    bucket = bucket_by_account_and_name(account, bucketName)
    bucket.perc_budget_amount = round(newAmount, 2)
    account.save()

    return bucket



def account_by_name(account_name: str) -> Account:
    return Account.objects(account_name=account_name).first()

def accounts_as_dict() -> Dict[int, str]:
    accounts = query_account('')
    return {i + 1: accounts[i].account_name for i in range(0, len(accounts))}

def query_account(query, accountNames: List[str] = None) -> List[Account]:

    if accountNames is None:
        accounts = Account.objects()
    else:
        accounts = Account.objects().filter(account_name__in=accountNames)

    if query == "":
        return accounts.order_by('date_stamp')
    else:
        return accounts.filter(__raw__=query).order_by('date_stamp')

def buckets_by_account(account:Account) -> List[Bucket]:

    buckets = Account.objects(id=account.id).first().buckets

    bucket_list =[
        bucket for bucket in buckets
    ]

    return bucket_list

    # return Account.objects(id=account.id).first().buckets.filter()

def buckets_as_dict_by_account(account: Account, exceptedValues = None) -> Dict[int, str]:
    if exceptedValues is None:
        exceptedValues = set()

    buckets = buckets_by_account(account)
    buckets = [bucket for bucket in buckets if bucket.name not in exceptedValues]
    return {i + 1: buckets[i].name for i in range(0, len(buckets))}

def bucket_by_name(account:Account, bucket_name: str) -> Bucket:
    return Bucket.objects()\
        .filter(name=bucket_name)\
        .filter(account__name=account.name).first()

def spend_category_by_bucket_name(account:Account, bucket_name) -> str:
    return bucket_by_name(account, bucket_name).spend_category


def delete_bucket_from_account(account, bucketName):
    bucket = bucket_by_name(account, bucketName)
    bucket.delete()