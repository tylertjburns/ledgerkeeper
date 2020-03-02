from mongoData.ledger import LedgerItem
from mongoengine.queryset.visitor import Q
import datetime
from typing import List


def enter_if_not_exists(
    transaction_id: str,
    description: str,
    transaction_category: str,
    debit: float,
    credit: float,
    from_account: str,
    from_bucket: str,
    to_account: str,
    to_bucket: str,
    spend_category: str,
    date_stamp: datetime.datetime = datetime.datetime.now,
    notes: str = "",
    source: str = "")->LedgerItem:


    ledgers = find_ledger_by_description_date_debit_credit(description, date_stamp, debit, credit)

    if len(ledgers) > 0:
        return None
    else:
        return enter_ledger_entry(transaction_id
                            , description
                            , transaction_category
                            , debit
                            , credit
                            , from_account
                            , from_bucket
                            , to_account
                            , to_bucket
                            , spend_category=spend_category
                            , date_stamp=date_stamp
                            , notes=notes
                            , source=source)


def enter_ledger_entry(transaction_id: str,
    description: str,
    transaction_category: str,
    debit: float,
    credit: float,
    from_account: str,
    from_bucket: str,
    to_account: str,
    to_bucket: str,
    spend_category: str,
    date_stamp: datetime.datetime = datetime.datetime.now,
    notes: str = "",
    source: str = "") -> LedgerItem:

    ledger = LedgerItem()
    ledger.transaction_id = transaction_id
    ledger.transaction_category = transaction_category
    ledger.description = description
    ledger.debit = round(debit, 2)
    ledger.credit = round(credit, 2)
    ledger.from_account = from_account
    ledger.from_bucket = from_bucket
    ledger.to_account = to_account
    ledger.to_bucket = to_bucket
    ledger.date_stamp = date_stamp
    ledger.spend_category = spend_category
    ledger.notes = notes
    ledger.source = source

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

def find_ledger_by_date_debit_credit(date: datetime.date, debit: float = 0, credit:float = 0) -> List[LedgerItem]:
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

def query_ledger(query) -> List[LedgerItem]:
    if query == "":
        return LedgerItem.objects().order_by('date_stamp')
    else:
        return LedgerItem.obects(__raw__=query).order_by('date_stamp')

def delete_by_id(id: str):
    success = LedgerItem.objects(id=id).delete()
    return success

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
    
    ret = ledger_by_account("aa1")
    print (f"#: {len(ret)} \n{ret.to_json()}")