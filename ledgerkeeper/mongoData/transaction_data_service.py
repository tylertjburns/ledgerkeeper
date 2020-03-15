from ledgerkeeper.interfaces.ITransactionDataService import ITransactionDataService
from ledgerkeeper.mongoData.transaction import Transaction
from ledgerkeeper.enums import TransactionStatus, TransactionTypes, TransactionSource, PaymentType
import datetime
from typing import List

class TransactionDataService(ITransactionDataService):

    def enter_if_not_exists(self,
                            transaction_id: str,
                            description: str,
                            transaction_category: TransactionTypes,
                            debit: float,
                            credit: float,
                            source: TransactionSource,
                            payment_type: PaymentType,
                            date_stamp: datetime.datetime = datetime.datetime.now,
                            handled: TransactionStatus = TransactionStatus.UNHANDLED) -> Transaction:

        transactions = self.find_by_description_date_debit_credit(description, date_stamp, debit, credit)

        if len(transactions) > 0:
            return None
        else:
            return self.enter_transaction(transaction_id=transaction_id
                                      , description=description
                                      , transaction_category=transaction_category
                                      , debit=debit
                                      , credit=credit
                                      , source=source
                                      , date_stamp=date_stamp
                                      , handled=handled
                                      , payment_type=payment_type
                                     )

    def enter_transaction(self, transaction_id: str,
        description: str,
        transaction_category: TransactionTypes,
        debit: float,
        credit: float,
        source: TransactionSource,
        payment_type: PaymentType,
        date_stamp: datetime.datetime = datetime.datetime.now,
        handled:TransactionStatus = TransactionStatus.UNHANDLED) -> Transaction:

        transaction = Transaction()
        transaction.id = transaction_id
        transaction.category = transaction_category.name
        transaction.description = description
        transaction.debit = debit
        transaction.credit = credit
        transaction.date_stamp = date_stamp
        transaction.source = source.name
        transaction.handled = handled.name
        transaction.payment_type = payment_type.name
        transaction.save()

        return transaction

    def query(self, query) -> List[Transaction]:
        if query == "":
            return Transaction.objects().order_by('date_stamp')
        else:
            return Transaction.obects(__raw__=query).order_by('date_stamp')

    def unhandled_transactions(self) -> List[Transaction]:
        return Transaction.objects(handled=TransactionStatus.UNHANDLED.name).order_by('date_stamp')

    def clear_collection(self):
        Transaction.drop_collection()


    def find_by_description_date_debit_credit(self, description: str, date: datetime.date, debit: float = 0,
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

    def mark_transaction_handled(self, transaction: Transaction, status=TransactionStatus.HANDLED) -> Transaction:
        return Transaction.objects(transaction_id=transaction.id).update_one(handled=status.name)



