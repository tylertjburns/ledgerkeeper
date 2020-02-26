from mongoData.transaction import Transaction
import datetime
from typing import List


def enter_if_not_exists(transaction_id: str,
    description: str,
    transaction_category: str,
    debit: float,
    credit: float,
    source: str,
    date_stamp: datetime.datetime = datetime.datetime.now) -> Transaction:

    transactions = find_by_description_date_debit_credit(description, date_stamp, debit, credit)

    if len(transactions) > 0:
        return None
    else:
        return enter_transaction(transaction_id
                                  , description
                                  , transaction_category
                                  , debit
                                  , credit
                                  , source
                                  , date_stamp
                                 )

def enter_transaction(transaction_id: str,
    description: str,
    transaction_category: str,
    debit: float,
    credit: float,
    source: str,
    date_stamp: datetime.datetime = datetime.datetime.now) -> Transaction:

    transaction = Transaction()
    transaction.id = transaction_id
    transaction.category = transaction_category
    transaction.description = description
    transaction.debit = debit
    transaction.credit = credit
    transaction.date_stamp = date_stamp
    transaction.source = source

    transaction.save()

    return transaction

def query(query) -> List[Transaction]:
    if query == "":
        return Transaction.objects().order_by('date_stamp')
    else:
        return Transaction.obects(__raw__=query).order_by('date_stamp')

def unhandled_transactions() -> List[Transaction]:
    return Transaction.objects(handled=0).order_by('date_stamp')

def clear_collection():
    Transaction.drop_collection()


def find_by_description_date_debit_credit(description: str, date: datetime.date, debit: float = 0,
                                                 credit: float = 0) -> List[Transaction]:
    start = date
    end = date + datetime.timedelta(days=1)

    query = Transaction.objects() \
        .filter(description=description) \
        .filter(date_stamp__gte=start) \
        .filter(date_stamp__lte=end) \
        .filter(debit=debit) \
        .filter(credit=credit)

    transactions = query.order_by('date_stamp')

    return transactions

def mark_transaction_handled(transaction: Transaction, status=1) -> Transaction:
    Transaction.objects(transaction_id=transaction.id).update_one(handled=status)
