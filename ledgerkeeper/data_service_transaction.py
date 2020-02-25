from mongoData.transaction import Transaction
import datetime

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
