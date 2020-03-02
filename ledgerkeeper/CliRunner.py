import mongoData.ledger_data_service as dsvcl
from mongoData.transaction import Transaction
import mongoData.transaction_data_service as dsvct
import mongoData.account_data_service as dsvca

import dataFileTranslation as dft
from enums import TransactionSource, TransactionTypes, CollectionType, TransactionStatus, TransactionSplitType, AccountType, SpendCategory
import uuid

from plotter import plot_history_by_category
from cliHelper import _notify_user, \
    _request_filepath,\
    _request_from_dict, \
    _request_enum, \
    _request_float, \
    _request_int, \
    _request_date,\
    _pretty_print_items


NOTIMPLEMENTED = "-------------- NOT IMPLEMENTED ----------------"


def request_action():
    print('*******************************************************')

    print("Which action would you like to take?")

    print("LEDGER ITEMS")
    print("[A]dd new ledger entry manually")
    print("[Q]uery ledger")
    print("[D]elete a ledger item")
    print("")

    print("TRANSACTIONS")
    print("[L]oad transactions")
    print("P[R]ocess new transactions")
    print("")

    print("BUCKETS")
    print("Add Buc[K]et to account")
    print("")

    print("ADMIN")
    print("Add [N]ew Account")
    print("[C]lear Collection")
    print("[P]rint Collection")
    print("Pl[O]t options")
    print("E[X]it")
    print("")
    return input("").upper()

def action_switch(input: str):
    switcher = {
        "A": add_ledger,
        "C": clear_collection,
        "D": delete_a_ledger_item,
        "G": get_new_item,
        "K": add_bucket_to_account,
        'L': load_new_transactions,
        'N': add_new_account,
        'O': plot_request_loop,
        "P": print_collection,
        "Q": query_ledger,
        "R": process_transactions_loop,
        "X": exit_app
    }

    return switcher.get(input, None)

def request_transaction_action():
    print("What do you want to do with this transaction?")

    print("[A]pprove")
    print("[D]eny")
    print("[S]plit")
    print("Mark D[U]plicate")
    print("[B]ack to main menu")
    print("")
    return input("").upper()

def process_transaction_switch(input: str):
    switcher = {
        "A": approve_transaction,
        "D": deny_transaction,
        "U": mark_transaction_duplicate,
        "S": split_transaction,
        "B": "return"
    }
    return switcher.get(input, None)


def plot_request_action():
    print("What do you want to plot?")

    print("[H]istory by Category")
    print("[B]ack to main menu")
    print("")
    return input("").upper()

def plot_switch(input: str):
    switcher = {
        "H": plot_history_by_category,
        "B": "return"
    }
    return switcher.get(input, None)

def add_new_account():
    print('******************** NEW ACCOUNT ********************')
    type = _request_enum(AccountType)
    name = input("Account Name:")
    description = input("Description:")

    account = dsvca.enter_if_not_exists(name=name, type=type, description=description)

    if account is not None:
        _notify_user("Account created successfully!")
    else:
        _notify_user(f"Error creating account. An account with the name {name} already exists.")


def add_ledger():
    print('******************** ADD LEDGER ********************')
    transaction_id = input("Transaction Id:")
    description = input("Description:")
    transaction_category = _request_enum(TransactionTypes)
    debit = _request_float("Debit:")
    credit = _request_float("Credit:")
    from_account = dsvca.accounts_as_dict("From Account:")
    from_bucket = _request_from_dict(dsvca.buckets_as_dict_by_account(from_account), "From Bucket:")
    to_account = dsvca.accounts_as_dict("To Account:")
    to_bucket = _request_from_dict(dsvca.buckets_as_dict_by_account(to_account), "To Bucket:")
    spend_category = _request_enum(SpendCategory)
    date_stamp = _request_date()
    notes = input("Notes:")

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
        print("Ledger item already exists")
    else:
        print("Ledger Entry added successfully")


def get_new_item():
    print('******************** GET NEW ITEM ********************')
    print(NOTIMPLEMENTED)

def query_ledger():
    print('******************** QUERY LEDGER ********************')
    query = input("Query:")
    dsvcl.query_ledger(query)


def print_collection():
    print('******************** PRINT ********************')

    print_type = _request_enum(CollectionType)

    if CollectionType[print_type] == CollectionType.LEDGER:
        items_json = dsvcl.query_ledger("").to_json()
        _pretty_print_items(items_json, title=CollectionType.LEDGER.name)
    elif CollectionType[print_type] == CollectionType.TRANSACTIONS:
        items_json = dsvct.query("").to_json()
        _pretty_print_items(items_json, title=CollectionType.TRANSACTIONS.name)
    elif CollectionType[print_type] == CollectionType.BUCKETS:
        account = _request_from_dict(dsvca.accounts_as_dict())
        _pretty_print_items(dsvca.buckets_by_account(dsvca.account_by_name(account)), title=CollectionType.BUCKETS.name)
    elif CollectionType[print_type] == CollectionType.ACCOUNTS:
        _pretty_print_items(dsvca.query_account("").to_json(), title=CollectionType.ACCOUNTS.name)
    else:
        print(NOTIMPLEMENTED)


    print("")

def clear_collection():
    print('******************** CLEAR COLLECTION ********************')
    collection = _request_enum(CollectionType)

    if CollectionType[collection] == CollectionType.LEDGER:
        dsvcl.clear_ledger()
    elif CollectionType[collection] == CollectionType.TRANSACTIONS:
        dsvct.clear_collection()
    else:
        print(NOTIMPLEMENTED)

    _notify_user(f"{collection} collection cleared\n")

def delete_a_ledger_item():
    print('******************** DELETE A LEDGER ITEM ********************')
    id = input("ID:")

    success = dsvcl.delete_by_id(id)
    if success == 1:
        _notify_user(f"Ledger item {id} deleted")
    else:
        _notify_user(f"Ledger with id {id} not found")

def exit_app():
    print('******************** EXIT APP ********************')
    _notify_user("Goodbye!!")
    raise KeyboardInterrupt()

def process_transaction(transaction: Transaction):
    # Print the Transaction
    _pretty_print_items(transaction.to_json(), title="Transaction to Handle")
    print("")

    # Show potential duplicates
    _pretty_print_items(
        dsvcl.find_ledger_by_date_debit_credit(transaction.date_stamp, transaction.debit, transaction.credit).to_json()
        , title="Potential Duplicates")
    print("")

    while True:
        # Request direction from user
        action = process_transaction_switch(request_transaction_action())

        # Process input
        if action is None:
            # Invalid entry
            _notify_user("Invalid Entry...")
        elif action == 'return':
            # Return early if the user wants
            return False
        else:
            # Process valid action on transaction
            action(transaction)
            return True



def plot_request_loop():
    print('******************** Plotting ********************')

    while True:
        # Request direction from user
        action = plot_switch(plot_request_action())

        # Process input
        if action is None:
            # Invalid entry
            _notify_user("Invalid Entry...")
        elif action == 'return':
            # Return early if the user wants
            return False
        else:
            # Process valid action on transaction
            action()
            return True

def process_transactions_loop():
    print('******************** Process Transaction ********************')

    # Enter loop for processing transactions
    while True:
        # Get all unhandled transactions
        unhandled_transactions = dsvct.unhandled_transactions()
        if unhandled_transactions is None or len(unhandled_transactions) == 0:
            break

        # Select and Print the transaction
        transaction = unhandled_transactions[0]
        result = process_transaction(transaction)
        if not result:
            return

    # Signal that all transactions have been handled
    _notify_user("No more transactions to process")



def load_new_transactions():
    print('******************** Load New Transactions ********************')

    # Ask User for source
    source = _request_enum(TransactionSource)

    # Get Filepath
    in_path = _request_filepath()

    # React to user input
    if TransactionSource[source] == TransactionSource.BARCLAYCARDUS:
        transactions = dft.read_in_barclay_transactions(in_path)
    elif TransactionSource[source] == TransactionSource.PNC:
        transactions = dft.read_in_pnc_transactions(in_path)
    elif TransactionSplitType[source] == TransactionSource.ARCHIVE:
        account = _request_from_dict(dsvca.accounts_as_dict())
        transactions = dft.read_in_old_ledgers(filepath=in_path, account=dsvca.account_by_name(account))
        _notify_user("Ledger Items created directly")
    else:
        print(NOTIMPLEMENTED)

    _notify_user(f"{len(transactions)} new Transactions from {source}")

def split_transaction(transaction: Transaction):

    input = _request_enum(TransactionSplitType)
    if transaction.credit > 0 and transaction.debit == 0:
        currentAmount= transaction.credit
    elif transaction.debit > 0 and transaction.credit == 0:
        currentAmount = transaction.debit
    else:
        raise NotImplementedError("Unable to handle transactions with both credit and debit values")

    if input == TransactionSplitType.PERCENTAGE.name:
        perc = _request_float("% of current to handle [0-100]:")
        amt = max(min(round(currentAmount * perc / 100, 2), currentAmount), 0)
    elif input == TransactionSplitType.DOLLAR.name:
        amt = max(min(_request_float(f"Amount to handle [up to {currentAmount}]:"), currentAmount), 0)
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

    _notify_user(f"Transaction Split into {newTransaction1.id} and {newTransaction2.id}")

def deny_transaction(transaction):
    dsvct.mark_transaction_handled(transaction, status=TransactionStatus.DENIED)
    _notify_user("Transaction denied...")
    
def mark_transaction_duplicate(transaction):
    dsvct.mark_transaction_handled(transaction, status=TransactionStatus.DUPLICATE)
    _notify_user("Marked as Duplicate...")

def approve_transaction(transaction):
    if transaction.credit > 0 and transaction.debit == 0:
        from_account = transaction.description
        from_bucket = "income_source"
        to_account = _request_from_dict(dsvca.accounts_as_dict(), prompt="To Account:")
        to_bucket = _request_from_dict(dsvca.buckets_as_dict_by_account(dsvca.account_by_name(to_account)), "To Bucket:")
        spend_category = "NA"
    elif transaction.credit == 0 and transaction.debit > 0:
        from_account = _request_from_dict(dsvca.accounts_as_dict(), prompt="From Account:")
        from_bucket = _request_from_dict(dsvca.buckets_as_dict_by_account(dsvca.account_by_name(from_account)), "From Bucket:")
        to_account = transaction.description
        to_bucket = "expense_source"
        spend_category = dsvca.spend_category_by_bucket_name(from_bucket)
    else:
        raise NotImplementedError(f"Unhandled combination of credit and debit values: debit [{transaction.debit}], credit [{transaction.credit}]")

    notes=input("Notes:")

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
        print("Ledger item already exists")
    else:
        _notify_user("Ledger Entry added successfully")
        dsvct.mark_transaction_handled(transaction)

def add_bucket_to_account():
    account = _request_from_dict(dsvca.accounts_as_dict(), prompt="Select an account:")
    name = input("Name:")
    prio = _request_int("Priority:")
    due_day = _request_int("Due day of month:")
    category = _request_enum(SpendCategory)
    base_budget_amount = _request_float("Base budget amount:")


    bucket = dsvca.add_bucket_to_account(dsvca.account_by_name(account_name=account)
                                , name=name
                                , priority=prio
                                , due_day_of_month=due_day
                                , spend_category=category
                                , base_budget_amount=base_budget_amount
                                )
    _notify_user(f"Bucket {bucket.name} added to {account} successfully.")


if __name__ == "__main__":
    import mongo_setup
    mongo_setup.global_init()

    while True:
        action = action_switch(request_action())
        if action is not None:
            action()
        else:
            _notify_user("Invalid Entry...")
