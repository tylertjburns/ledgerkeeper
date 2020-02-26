import data_service_ledger as dsvcl
import data_service_transaction as dsvct
import datetime

import time
import pandas as pd
import json
import dataFileTranslation as dft
from enum import Enum
from enums import TransactionSource, TransactionTypes, CollectionType

import tkinter
import tkinter.filedialog as fd



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

    print("ADMIN")
    print("[C]lear Collection")
    print("[P]rint Collection")
    print("E[X]it")
    print("")
    return input("").upper()

def action_switch(input: str):
    switcher = {
        "A": add_ledger,
        "D": delete_a_ledger_item,
        "G": get_new_item,
        'L': load_new_transactions,
        "Q": query_ledger,
        "P": print_collection,
        "C": clear_collection,
        "X": exit_app,
        "R": process_transactions_loop
    }

    return switcher.get(input, None)

def request_transaction_action():
    print("Which do you want to do with this transaction?")

    print("[A]pprove")
    print("[D]eny")
    print("[S]plit")
    print("[B]ack to main menu")
    print("")
    return input("").upper()

def process_transaction_switch(input: str):
    switcher = {
        "A": approve_transaction,
        "D": deny_transaction,
        "S": split_transaction,
        "B": "return"
    }
    return switcher.get(input, None)

def _request_float(prompt: str):
    while True:
        try:
            return float(input(prompt))
        except:
            print("invalid float format")
            time.sleep(1)

def _request_guid(prompt: str):
    while True:
        inp = input(prompt)
        if (len(inp)) == 24:
            return inp
        else:
            print("Invalid Guid...")
            time.sleep(1)

def _request_date():

    while True:
        inp = input("Enter date [Enter for current date]:")
        try:
            if inp == '':
                date_stamp = datetime.datetime.now()
                print(f"using: {date_stamp}")
            else:
                date_stamp = parser.parse(inp)
            break
        except:
            print("invalid date format")

    return date_stamp

def _request_enum(enum):
    while True:
        if issubclass(enum, Enum):
            inp = input(f"Enter {enum.__name__} {[i.name for i in enum]}:").upper()
            if not enum.has_value(inp):
                print(f"Invalid Entry. Select from {[i.name for i in enum]}")
            else:
                return inp
        else:
            raise TypeError(f"Input must be of type Enum but {type(enum)} was provided")


def _pretty_print_json_items(json_items):
    data = pd.io.json.json_normalize(json.loads(json_items))
    print(f"# of items {len(data)}")
    if len(data) > 0:
        with pd.option_context('display.max_columns', 2000, 'display.width', 250):
            print(data)

def add_ledger():
    print('******************** ADD LEDGER ********************')
    transaction_id = input("Transaction Id:")
    description = input("Description:")
    transaction_category = input("Transaction Category:")
    debit = _request_float("Debit:")
    credit = _request_float("Credit:")
    from_account = input("From Account:")
    from_bucket = input("From Bucket:")
    to_account = input("To Account:")
    to_bucket = input("To Bucket:")
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
                            , date_stamp
                            , notes)

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
        _pretty_print_json_items(items_json)
    elif CollectionType[print_type] == CollectionType.TRANSACTIONS:
        items_json = dsvct.query("").to_json()
        _pretty_print_json_items(items_json)
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

    print(f"{collection} collection cleared\n")
    time.sleep(1)

def delete_a_ledger_item():
    print('******************** DELETE A LEDGER ITEM ********************')
    id = input("ID:")

    success = dsvcl.delete_by_id(id)
    if success == 1:
        print(f"Ledger item {id} deleted")
    else:
        print(f"Ledger with id {id} not found")
        time.sleep(1)

def exit_app():
    print('******************** EXIT APP ********************')
    print("Goodbye!!")
    time.sleep(1)
    raise KeyboardInterrupt()

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
        _pretty_print_json_items(transaction.to_json())

        # Request direction from user
        action = process_transaction_switch(request_transaction_action())

        # Process input
        if action is None:
            # Invalid entry
            print("Invalid Entry...")
        elif action == 'return':
            # Return early if the user wants
            return
        else:
            # Process valid action on transaction
            action(transaction)

        time.sleep(1)

    # Signal that all transactions have been handled
    print("No more transactions to process")
    time.sleep(1)


def load_new_transactions():
    print('******************** Load New Transactions ********************')

    # Ask User for source
    source = _request_enum(TransactionSource)

    # Find File Path
    root = tkinter.Tk()
    in_path = fd.askopenfilename()

    # React to user input
    if TransactionSource[source] == TransactionSource.BARCLAYCARDUS:
        transactions = dft.read_in_barclay_transactions(in_path)
    elif TransactionSource[source] == TransactionSource.PNC:
        transactions = dft.read_in_pnc_transactions(in_path)
    else:
        print(NOTIMPLEMENTED)

    # Close TKinter app
    root.destroy()

    print(f"Number of New Transactions: {len(transactions)}")
    time.sleep(1)


def split_transaction(transaction):
    print(NOTIMPLEMENTED)

def deny_transaction(transaction):
    dsvct.mark_transaction_handled(transaction, status=-1)
    print("Transaction denied...")
    time.sleep(1)

def approve_transaction(transaction):

    if transaction.credit > 0 and transaction.debit == 0:
        from_account = transaction.description
        from_bucket = "income_source"
        to_account = input("To Account:")
        to_bucket = input("To Bucket:")
    elif transaction.credit == 0 and transaction.debit > 0:
        from_account = input("From Account:")
        from_bucket = input("From Bucket:")
        to_account = transaction.description
        to_bucket = "expense_source"
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
                                       , date_stamp=transaction.date_stamp
                                       , notes=notes)

    if ledger is None:
        print("Ledger item already exists")
    else:
        print("Ledger Entry added successfully")
        dsvct.mark_transaction_handled(transaction)


if __name__ == "__main__":
    import mongo_setup
    mongo_setup.global_init()

    while True:
        action = action_switch(request_action())
        if action is not None:
            action()
        else:
            print("Invalid Entry...")
            time.sleep(1)
