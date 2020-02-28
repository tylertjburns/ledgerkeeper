from mongoData.account import Account
from mongoData.bucket import Bucket
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
                          spend_category: str,
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
    bucket.spend_category = spend_category
    bucket.base_budget_amount = base_budget_amount
    bucket.perc_budget_amount = perc_budget_amount
    bucket.waterfall_amount = waterfall_amount
    bucket.saved_amount = saved_amount
    bucket.percent_of_income_adjustment_amount = percent_of_income_adjustment_amount

    account = Account.objects(id=account.id).first()
    account.buckets.append(bucket)
    account.save()

    return bucket

def account_by_name(account_name: str) -> Account:
    return Account.objects(account_name=account_name).first()

def accounts_as_dict() -> Dict[int, str]:
    accounts = query_account('')
    return {i + 1: accounts[i].account_name for i in range(0, len(accounts))}

def query_account(query) -> List[Account]:
    if query == "":
        return Account.objects().order_by('date_stamp')
    else:
        return Account.obects(__raw__=query).order_by('date_stamp')

def buckets_by_account(account:Account) -> List[Bucket]:

    buckets = Account.objects(id=account.id).first().buckets

    bucket_list =[
        bucket.to_json() for bucket in buckets
    ]

    return bucket_list

    # return Account.objects(id=account.id).first().buckets.filter()

def buckets_as_dict_by_account(account: Account) -> Dict[int, str]:
    buckets = buckets_by_account(account)
    return {i + 1: buckets[i].name for i in range(0, len(buckets))}
