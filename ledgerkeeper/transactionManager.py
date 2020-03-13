
from ledgerkeeper.enums import HandleTransactionMethod, TransactionTypes, TransactionStatus, \
    TransactionSplitType, SpendCategory, AccountStatus, PaymentType, TransactionSource
from enums import CollectionType
from ledgerkeeper.mongoData.transaction import Transaction
import ledgerkeeper.mongoData.transaction_data_service as dsvct
import ledgerkeeper.mongoData.account_data_service as dsvca
import ledgerkeeper.mongoData.ledger_data_service as dsvcl
from userInteraction.abstracts.financeInteraction import FinanceInteraction

import uuid

class TransactionManager():
    def __init__(self, user_notification_system: FinanceInteraction):
        self.uns = user_notification_system

    def print_transactions(self):
        items_json = dsvct.query("").to_json()
        self.uns.pretty_print_items(items_json, title=CollectionType.TRANSACTIONS.name)


    def process_transaction_switch(self, input: int):
        switcher = {
            HandleTransactionMethod.APPROVE.value: self.approve_transaction,
            HandleTransactionMethod.DENY.value: self.deny_transaction,
            HandleTransactionMethod.DUPLICATE.value: self.mark_transaction_duplicate,
            HandleTransactionMethod.SPLIT.value: self.split_transaction,
        }
        return switcher.get(input, None)

    def process_transaction(self, transaction):
        # Print the Transaction
        self.uns.pretty_print_items(transaction.to_json(), title="Transaction to Handle")
        print("")

        # Show potential duplicates
        self.uns.pretty_print_items(
            dsvcl.find_ledger_by_date_debit_credit(transaction.date_stamp, transaction.debit,
                                                   transaction.credit).to_json()
            , title="Potential Duplicates")
        print("")

        while True:
            # Request direction from user
            direction = self.uns.request_enum(HandleTransactionMethod, "What do you want to do with this transaction?")
            if direction is None:
                break

            action = self.process_transaction_switch(direction)

            # Process input
            if action is None:
                # Invalid entry
                self.uns.notify_user("Invalid Entry...")
            else:
                # Process valid action on transaction
                action(transaction)
                return True

    def process_transactions_loop(self):
        # Enter loop for processing transactions
        while True:
            # Get all unhandled transactions
            unhandled_transactions = dsvct.unhandled_transactions()
            if unhandled_transactions is None or len(unhandled_transactions) == 0:
                break

            # Select and Print the transaction
            transaction = unhandled_transactions[0]
            result = self.process_transaction(transaction)
            if not result:
                return

        # Signal that all transactions have been handled
        self.uns.notify_user("No more transactions to process")

    def split_transaction(self, transaction: Transaction):
        if transaction.credit > 0 and transaction.debit == 0:
            currentAmount = transaction.credit
        elif transaction.debit > 0 and transaction.credit == 0:
            currentAmount = transaction.debit
        else:
            raise NotImplementedError("Unable to handle transactions with both credit and debit values")

        amt = self.uns.get_split_transaction_input(currentAmount)

        if transaction.credit > 0:
            newdeb1 = 0.0
            newdeb2 = 0.0
            newcred1 = amt
            newcred2 = transaction.credit - amt
        elif transaction.debit > 0:
            newdeb1 = amt
            newdeb2 = transaction.debit - amt
            newcred1 = 0.0
            newcred2 = 0.0
        else:
            raise NotImplementedError("Unknown Scenario for splits")

        newTransaction1 = dsvct.enter_if_not_exists(transaction_category=transaction.category
                                                    , transaction_id=str(uuid.uuid4())
                                                    , description=transaction.description
                                                    , debit=newdeb1
                                                    , credit=newcred1
                                                    , source=transaction.source
                                                    , payment_type=transaction.payment_type
                                                    , date_stamp=transaction.date_stamp)
        newTransaction2 = dsvct.enter_if_not_exists(transaction_category=transaction.category
                                                    , transaction_id=str(uuid.uuid4())
                                                    , description=transaction.description
                                                    , debit=newdeb2
                                                    , credit=newcred2
                                                    , payment_type=transaction.payment_type
                                                    , source=transaction.source
                                                    , date_stamp=transaction.date_stamp)
        dsvct.mark_transaction_handled(transaction, TransactionStatus.SPLIT)

        self.uns.notify_user(f"Transaction Split into {newTransaction1.id} and {newTransaction2.id}")

    def deny_transaction(self, transaction):
        dsvct.mark_transaction_handled(transaction, status=TransactionStatus.DENIED)
        self.uns.notify_user("Transaction denied...")

    def mark_transaction_duplicate(self, transaction):
        dsvct.mark_transaction_handled(transaction, status=TransactionStatus.DUPLICATE)
        self.uns.notify_user("Marked as Duplicate...")

    def _enter_ledger_from_income_transaction(self, transaction:Transaction):
        from_account = transaction.description
        from_bucket = "income_source"
        input = self.uns.get_enter_ledger_from_income_transaction_input()
        to_account = input['to_account']
        to_bucket = input['to_bucket']
        spend_category = SpendCategory.NOTAPPLICABLE
        notes = input['notes']

        ledger = dsvcl.enter_if_not_exists(transaction_id=transaction.transaction_id
                                           , description=transaction.description
                                           , transaction_category=TransactionTypes[transaction.category]
                                           , debit=transaction.debit
                                           , credit=transaction.credit
                                           , from_account=from_account
                                           , from_bucket=from_bucket
                                           , to_account=to_account
                                           , to_bucket=to_bucket
                                           , spend_category=SpendCategory[spend_category]
                                           , payment_type=PaymentType[transaction.payment_type]
                                           , date_stamp=transaction.date_stamp
                                           , notes=notes
                                           , source=TransactionSource[transaction.source])

        return ledger

    def _enter_ledger_from_expense_transaction(self, transaction:Transaction):
        input = self.uns.get_enter_ledger_from_expense_transaction_input()
        from_account = input['from_account']
        from_bucket = input['from_bucket']
        to_account = transaction.description
        to_bucket = "expense_source"
        spend_category = dsvca.spend_category_by_bucket_name(account=from_account, bucket_name=from_bucket.name)
        notes = input['notes']


        ledger = dsvcl.enter_if_not_exists(transaction_id=transaction.transaction_id
                                           , description=transaction.description
                                           , transaction_category=TransactionTypes[transaction.category]
                                           , debit=transaction.debit
                                           , credit=transaction.credit
                                           , from_account=from_account
                                           , from_bucket=from_bucket
                                           , to_account=to_account
                                           , to_bucket=to_bucket
                                           , spend_category=SpendCategory[spend_category]
                                           , payment_type=PaymentType[transaction.payment_type]
                                           , date_stamp=transaction.date_stamp
                                           , notes=notes
                                           , source=TransactionSource[transaction.source])

        return ledger

    def approve_transaction(self, transaction):
        if transaction.credit > 0 and transaction.debit == 0:
            ledger = self._enter_ledger_from_income_transaction(transaction)
        elif transaction.credit == 0 and transaction.debit > 0:
            ledger = self._enter_ledger_from_expense_transaction(transaction)
        else:
            raise NotImplementedError(
                f"Unhandled combination of credit and debit values: debit [{transaction.debit}], credit [{transaction.credit}]")

        if ledger is None:
            self.uns.notify_user("Ledger item already exists")
        else:
            self.uns.notify_user("Ledger Entry added successfully")
            dsvct.mark_transaction_handled(transaction)

        return ledger
