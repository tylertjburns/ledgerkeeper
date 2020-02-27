from mongoData.account import Account
from typing import List

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

def query(query) -> List[Account]:
    if query == "":
        return Account.objects().order_by('date_stamp')
    else:
        return Account.obects(__raw__=query).order_by('date_stamp')