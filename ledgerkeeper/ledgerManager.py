
from enums import TransactionSource, TransactionTypes, CollectionType, TransactionStatus, TransactionSplitType, AccountType, SpendCategory
from mongoData.transaction import Transaction
import mongoData.transaction_data_service as dsvct
import mongoData.account_data_service as dsvca
import mongoData.ledger_data_service as dsvcl
from abstracts.userInteractionManager import UserIteractionManager
import uuid

from plotter import plot_history_by_category

RELEVANTMONTHS = 10

class LedgerManager():
    def __init__(self, user_notification_system: UserIteractionManager):
        self.uns = user_notification_system

    def add_new_account(self):
        type = self.uns.request_enum(AccountType)
        name = self.uns.request_string("Account Name:")
        description = self.uns.request_string("Description:")

        account = dsvca.enter_if_not_exists(name=name, type=type, description=description)

        if account is not None:
            self.uns.notify_user("Account created successfully!")
        else:
            self.uns.notify_user(f"Error creating account. An account with the name {name} already exists.")

    def add_ledger(self):
        transaction_id = self.uns.request_string("Transaction Id:")
        description = self.uns.request_string("Description:")
        transaction_category = self.uns.request_enum(TransactionTypes)
        debit = self.uns.request_float("Debit:")
        credit = self.uns.request_float("Credit:")
        from_account = dsvca.accounts_as_dict("From Account:")
        from_bucket = self.uns.request_from_dict(dsvca.buckets_as_dict_by_account(from_account), "From Bucket:")
        to_account = dsvca.accounts_as_dict("To Account:")
        to_bucket = self.uns.request_from_dict(dsvca.buckets_as_dict_by_account(to_account), "To Bucket:")
        spend_category = self.uns.request_enum(SpendCategory)
        date_stamp = self.uns.request_date()
        notes = self.uns.request_string("Notes:")

        ledger = dsvcl.enter_if_not_exists(transaction_id
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
                                           , notes=notes)

        if ledger is None:
            self.uns.notify_user("Ledger item already exists")
        else:
            self.uns.notify_user("Ledger Entry added successfully")

    def query_ledger(self):
        query = self.uns.request_string("Query:")
        dsvcl.query_ledger(query)

    def print_collection(self):
        print_type = self.uns.request_enum(CollectionType)

        if CollectionType[print_type] == CollectionType.LEDGER:
            items_json = dsvcl.query_ledger("").to_json()
            self.uns.pretty_print_items(items_json, title=CollectionType.LEDGER.name)
        elif CollectionType[print_type] == CollectionType.TRANSACTIONS:
            items_json = dsvct.query("").to_json()
            self.uns.pretty_print_items(items_json, title=CollectionType.TRANSACTIONS.name)
        elif CollectionType[print_type] == CollectionType.BUCKETS:
            account = self.uns.request_from_dict(dsvca.accounts_as_dict())
            self.uns.pretty_print_items(dsvca.buckets_by_account(dsvca.account_by_name(account)),
                                title=CollectionType.BUCKETS.name)
        elif CollectionType[print_type] == CollectionType.ACCOUNTS:
            self.uns.pretty_print_items(dsvca.query_account("").to_json(), title=CollectionType.ACCOUNTS.name)
        else:
            raise NotImplementedError(f"No print type setup for {print_type}")

        print("")

    def clear_collection(self):
        collection = self.uns.request_enum(CollectionType)

        if CollectionType[collection] == CollectionType.LEDGER:
            dsvcl.clear_ledger()
        elif CollectionType[collection] == CollectionType.TRANSACTIONS:
            dsvct.clear_collection()
        else:
            raise NotImplementedError(f"Undefined collection for clearing {collection}")

        self.uns.notify_user(f"{collection} collection cleared\n")

    def delete_a_ledger_item(self):
        id = self.uns.request_string("ID:")

        success = dsvcl.delete_by_id(id)
        if success == 1:
            self.uns.notify_user(f"Ledger item {id} deleted")
        else:
            self.uns.notify_user(f"Ledger with id {id} not found")


    def process_transaction_switch(self, input: str):
        switcher = {
            "A": self.approve_transaction,
            "D": self.deny_transaction,
            "U": self.mark_transaction_duplicate,
            "S": self.split_transaction,
            "B": "return"
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
            action = self.process_transaction_switch(self.uns.request_transaction_action())

            # Process input
            if action is None:
                # Invalid entry
                self.uns.notify_user("Invalid Entry...")
            elif action == 'return':
                # Return early if the user wants
                return False
            else:
                # Process valid action on transaction
                action(transaction)
                return True


    def plot_switch(self, input: str):
        switcher = {
            "H": plot_history_by_category,
            "B": "return"
        }
        return switcher.get(input, None)

    def plot_request_loop(self):
        while True:
            # Request direction from user
            action = self.plot_switch(self.uns.plot_request_action())

            # Process input
            if action is None:
                # Invalid entry
                self.uns.notify_user("Invalid Entry...")
            elif action == 'return':
                # Return early if the user wants
                return False
            else:
                # Process valid action on transaction
                action(RELEVANTMONTHS)
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
        input = self.uns.request_enum(TransactionSplitType)
        if transaction.credit > 0 and transaction.debit == 0:
            currentAmount = transaction.credit
        elif transaction.debit > 0 and transaction.credit == 0:
            currentAmount = transaction.debit
        else:
            raise NotImplementedError("Unable to handle transactions with both credit and debit values")

        if input == TransactionSplitType.PERCENTAGE.name:
            perc = self.uns.request_float("% of current to handle [0-100]:")
            amt = max(min(round(currentAmount * perc / 100, 2), currentAmount), 0)
        elif input == TransactionSplitType.DOLLAR.name:
            amt = max(min(self.uns.request_float(f"Amount to handle [up to {currentAmount}]:"), currentAmount), 0)
        else:
            raise NotImplementedError(f"{input} is not implemented as a TransactionSplitType")

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
                                                    , date_stamp=transaction.date_stamp)
        newTransaction2 = dsvct.enter_if_not_exists(transaction_category=transaction.category
                                                    , transaction_id=str(uuid.uuid4())
                                                    , description=transaction.description
                                                    , debit=newdeb2
                                                    , credit=newcred2
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

    def approve_transaction(self, transaction):
        if transaction.credit > 0 and transaction.debit == 0:
            from_account = transaction.description
            from_bucket = "income_source"
            to_account = self.uns.request_from_dict(dsvca.accounts_as_dict(), prompt="To Account:")
            to_bucket = self.uns.request_from_dict(dsvca.buckets_as_dict_by_account(dsvca.account_by_name(to_account)),
                                           "To Bucket:")
            spend_category = "NA"
        elif transaction.credit == 0 and transaction.debit > 0:
            from_account = self.uns.request_from_dict(dsvca.accounts_as_dict(), prompt="From Account:")
            from_bucket = self.uns.request_from_dict(dsvca.buckets_as_dict_by_account(dsvca.account_by_name(from_account)),
                                             "From Bucket:")
            to_account = transaction.description
            to_bucket = "expense_source"
            spend_category = dsvca.spend_category_by_bucket_name(from_bucket)
        else:
            raise NotImplementedError(
                f"Unhandled combination of credit and debit values: debit [{transaction.debit}], credit [{transaction.credit}]")

        notes = self.uns.request_string("Notes:")

        ledger = dsvcl.enter_if_not_exists(transaction_id=transaction.transaction_id
                                           , description=transaction.description
                                           , transaction_category=transaction.category
                                           , debit=transaction.debit
                                           , credit=transaction.credit
                                           , from_account=from_account
                                           , from_bucket=from_bucket
                                           , to_account=to_account
                                           , to_bucket=to_bucket
                                           , spend_category=spend_category
                                           , date_stamp=transaction.date_stamp
                                           , notes=notes
                                           , source=transaction.source)

        if ledger is None:
            self.uns.notify_user("Ledger item already exists")
        else:
            self.uns.notify_user("Ledger Entry added successfully")
            dsvct.mark_transaction_handled(transaction)

    def add_bucket_to_account(self):
        account = self.uns.request_from_dict(dsvca.accounts_as_dict(), prompt="Select an account:")
        name = self.uns.request_string("Name:")
        prio = self.uns.request_int("Priority:")
        due_day = self.uns.request_int("Due day of month:")
        category = self.uns.request_enum(SpendCategory)
        base_budget_amount = self.uns.request_float("Base budget amount:")

        bucket = dsvca.add_bucket_to_account(dsvca.account_by_name(account_name=account)
                                             , name=name
                                             , priority=prio
                                             , due_day_of_month=due_day
                                             , spend_category=category
                                             , base_budget_amount=base_budget_amount
                                             )
        self.uns.notify_user(f"Bucket {bucket.name} added to {account} successfully.")