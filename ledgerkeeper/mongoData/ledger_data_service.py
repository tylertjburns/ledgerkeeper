from ledgerkeeper.mongoData.ledger import LedgerItem
from ledgerkeeper.mongoData.account import Account
from mongoengine.queryset.visitor import Q
import datetime
from typing import List
from ledgerkeeper.enums import TransactionTypes, TransactionSource, SpendCategory, TransactionTypes, PaymentType
import pandas as pd

def enter_if_not_exists(
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

    ledgers = find_ledger_by_description_date_debit_credit(description, date_stamp, debit, credit)

    if len(ledgers) > 0:
        return None
    else:
        return enter_ledger_entry(transaction_id=transaction_id
                                  , description=description
                                  , transaction_category=transaction_category
                                  , debit=debit
                                  , credit=credit
                                  , from_account=from_account
                                  , from_bucket=from_bucket
                                  , to_account=to_account
                                  , to_bucket=to_bucket
                                  , spend_category=spend_category
                                  , payment_type=payment_type
                                  , date_stamp=date_stamp
                                  , notes=notes
                                  , source=source)


def enter_ledger_entry(transaction_id: str,
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

    ledger = LedgerItem()
    ledger.transaction_id = transaction_id
    ledger.transaction_category = transaction_category.name
    ledger.description = description
    ledger.debit = round(debit, 2)
    ledger.credit = round(credit, 2)
    ledger.from_account = from_account
    ledger.from_bucket = from_bucket
    ledger.to_account = to_account
    ledger.to_bucket = to_bucket
    ledger.date_stamp = date_stamp
    ledger.spend_category = spend_category.name
    ledger.payment_type = payment_type.name
    ledger.notes = notes
    ledger.source = source.name

    ledger.save()

    return ledger

def ledger_by_account(account: str) -> List[LedgerItem]:
    return LedgerItem.objects().filter(Q(from_account=account) | Q(to_account=account))

def find_ledger_by_description_date_debit_credit(description: str
                                                 , date: datetime.date
                                                 , debit: float = 0
                                                 , credit: float = 0) -> LedgerItem:

    start = date
    end = date + datetime.timedelta(days=1)

    query = LedgerItem.objects() \
        .filter(description=description) \
        .filter(date_stamp__gte=start) \
        .filter(date_stamp__lte=end) \
        .filter(debit=debit) \
        .filter(credit=credit)

    ledgers = query.order_by('date_stamp')

    return ledgers

def find_ledger_by_date_debit_credit(date: datetime.date, debit: float = 0, credit: float = 0) -> List[LedgerItem]:
    start = date
    end = date + datetime.timedelta(days=1)

    query = LedgerItem.objects() \
        .filter(date_stamp__gte=start) \
        .filter(date_stamp__lte=end) \
        .filter(debit=debit) \
        .filter(credit=credit)

    ledgers = query.order_by('date_stamp')

    return ledgers

def clear_ledger():
    LedgerItem.drop_collection()

def query_ledger(query, raw_return=True, account_names: List[str] = None):

    if account_names is None:
        ledgers = LedgerItem.objects()
    else:
        query = Q(from_account__in=account_names) | Q(to_account__in=account_names)
        query = query.to_query(LedgerItem)
        ledgers = LedgerItem.objects().filter(__raw__=query)


    if raw_return:
        return ledgers.as_pymongo()
    else:
        ret_ledgers = []
        for l in ledgers.order_by('date_stamp'):
            ret_ledgers.append(l)

        return ret_ledgers


def delete_by_id(ledger_id: str):
    success = LedgerItem.objects(id=ledger_id).delete()
    return success

def expense_history(start_date, end_date, account: Account = None):
    if account is None:
        data = pd.DataFrame(query_ledger(""))
    else:
        data = pd.DataFrame(query_ledger("", account_names=[account.account_name]))

    if len(data) == 0:
        return pd.DataFrame(columns=['date_stamp', 'transaction_category', 'credit', 'amount_covered', 'refunded', 'spend_category'])

    spent = data[(data['transaction_category'] == TransactionTypes.RECORD_EXPENSE.name)
                 & (data['date_stamp'] >= pd.Timestamp(start_date))
                 & (data['date_stamp'] < pd.Timestamp(end_date))][['date_stamp', 'debit', 'amount_covered', 'refunded',
                                                                   'spend_category']]
    spent.index = spent['date_stamp']
    return spent

def income_history(start_date, end_date):
    data = pd.DataFrame(query_ledger(""))
    inc = data[(data['transaction_category'] == TransactionTypes.APPLY_INCOME.name)
               & (data['date_stamp'] >= pd.Timestamp(start_date))
               & (data['date_stamp'] < pd.Timestamp(end_date))][['date_stamp', 'credit']]
    inc.index = inc['date_stamp']
    return inc

if __name__ == "__main__":

    import mongo_setup
    mongo_setup.global_init()


    # # clear_ledger()
    # 
    # transaction_id = '1'
    # description = 'my desc'
    # transaction_category = "cat1"
    # debit = 1
    # credit = 100
    # from_account = "faccount"
    # to_account = "taccount"
    # from_bucket = "fbucket"
    # to_bucket = "tbucket"
    # date_stamp = datetime.datetime.now()
    # notes = "notesnotesnotesnotesnotes"
    # #
    # # enter_ledger_entry(transaction_id, description, transaction_category, debit,
    # #     credit, from_account, from_bucket, to_account, to_bucket, date_stamp, notes)
    # 
    # ret = find_ledger_by_description_date_debit(description, date_stamp, debit)
    # print(ret)
    
    # ret = ledger_by_account("aa1")
    ret = income_history(datetime.datetime.now() - datetime.timedelta(days=30), datetime.datetime.now())

    print(ret)

    print (f"#: {len(ret)} \n{ret.to_json()}")