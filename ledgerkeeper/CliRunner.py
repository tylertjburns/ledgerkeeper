import data_service_ledger as dsvcl
import data_service_transaction as dsvct
import datetime

import time
import pandas as pd
import json
import dataFileTranslation as dft
from enum import Enum
from enums import TransactionSource, TransactionTypes

import tkinter
import tkinter.filedialog as fd



NOTIMPLEMENTED = "-------------- NOT IMPLEMENTED ----------------"



def request_action():
    print('*******************************************************')

    print("Which action would you like to take?")

    print("LEDGER ITEMS")
    print("[A]dd new ledger entry manually")
    print("[Q]uery ledger")
    print("[P]rint ledger")
    print("[D]elete a ledger item")
    print("[C]lear ledger")
    print("")

    print("TRANSACTIONS")
    print("[L]oad transactions")
    print("P[R]ocess new transactions")
    print("")

    print("ADMIN")
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
        "P": print_ledger,
        "C": clear_ledger,
        "X": exit_app,
        "R": process_transaction
    }

    return switcher.get(input, None)

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

    return dsvcl.enter_ledger_entry(transaction_id
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

def get_new_item():
    print('******************** GET NEW ITEM ********************')
    print(NOTIMPLEMENTED)

def query_ledger():
    print('******************** QUERY LEDGER ********************')
    query = input("Query:")
    dsvcl.query_ledger(query)

def print_ledger():
    print('******************** PRINT LEDGER ********************')
    items_json = dsvcl.query_ledger("").to_json()

    data = pd.io.json.json_normalize(json.loads(items_json))
    print(f"# of items {len(data)}")
    if len(data) > 0:
        with pd.option_context('display.max_columns', 2000, 'display.width', 250):
            print(data)
    print("")

def clear_ledger():
    print('******************** CLEAR LEDGER ********************')
    dsvcl.clear_ledger()
    print("Ledger Cleared\n")

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

def process_transaction():
    print('******************** Process Transaction ********************')
    print(NOTIMPLEMENTED)

def load_new_transactions():
    print('******************** Load New Transactions ********************')

    root = tkinter.Tk()


    source = _request_enum(TransactionSource)
    in_path = fd.askopenfilename()
    print(source)
    if TransactionSource[source] == TransactionSource.BARCLAYCARDUS:
        dft.read_in_barclay_transactions(in_path)
    elif TransactionSource[source] == TransactionSource.PNC:
        dft.read_in_pnc_transactions(in_path)
    else:
        print(NOTIMPLEMENTED)

    root.destroy()

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
