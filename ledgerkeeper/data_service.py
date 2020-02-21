from mongoData.ledger import LedgerItem
import datetime
from typing import List

def enter_ledger_entry(transaction_id: str,
    description: str,
    transaction_category: str,
    debit: float,
    credit: float,
    from_account: str,
    from_bucket: str,
    to_account: str,
    to_bucket: str,
    date_stamp: datetime.datetime = datetime.datetime.now,
    notes: str = "") -> LedgerItem:

    ledger = LedgerItem()
    ledger.transaction_id = transaction_id
    ledger.transaction_category = transaction_category
    ledger.description = description
    ledger.debit = debit
    ledger.credit = credit
    ledger.from_account = from_account
    ledger.from_bucket = from_bucket
    ledger.to_account = to_account
    ledger.to_bucket = to_bucket
    ledger.date_stamp = date_stamp
    ledger.notes = notes

    ledger.save()

    return ledger

def find_ledger_by_description_date_debit(description: str, date: datetime.date, debit: float) -> LedgerItem:

    start = date
    end = date + datetime.timedelta(days=1)

    query = LedgerItem.objects() \
            .filter(description=description) \
            .filter(date_stamp__gte=start) \
            .filter(date_stamp__lte=end) \
            .filter(debit=debit) \

    ledgers = query.order_by('date_stamp')

    return ledgers

def clear_ledger():
    LedgerItem.drop_collection()

def query_ledger(query) -> List[LedgerItem]:
    return LedgerItem.obects(__raw__=query)

if __name__ == "__main__":

    import mongo_setup
    mongo_setup.global_init()
    # clear_ledger()

    transaction_id = '1'
    description = 'my desc'
    transaction_category = "cat1"
    debit = 1
    credit = 100
    from_account = "faccount"
    to_account = "taccount"
    from_bucket = "fbucket"
    to_bucket = "tbucket"
    date_stamp = datetime.datetime.now()
    notes = "notesnotesnotesnotesnotes"
    #
    # enter_ledger_entry(transaction_id, description, transaction_category, debit,
    #     credit, from_account, from_bucket, to_account, to_bucket, date_stamp, notes)

    ret = find_ledger_by_description_date_debit(description, date_stamp, debit)
    print(ret)