import data_service as dsvc
import datetime
from dateutil import parser
import time
import pandas as pd
import tabulate
import json

NOTIMPLEMENTED = "-------------- NOT IMPLEMENTED ----------------"



def request_action():
    print('*******************************************************')

    print("Which action would you like to take?")
    print("[A]dd new ledger entry manually")
    print("[G]et new ledger entry")
    print("[Q]uery ledger")
    print("[P]rint ledger")
    print("[C]lear ledger")
    print("E[X]it")
    print("")
    return input("").upper()

def action_switch(input: str):
    switcher = {
        "A": add_ledger,
        "G": get_new_item,
        "Q": query_ledger,
        "P": print_ledger,
        "C": clear_ledger,
        "X": exit_app,
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

    return dsvc.enter_ledger_entry(transaction_id
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

def get_new_item():
    print('******************** GET NEW ITEM ********************')
    print(NOTIMPLEMENTED)

def query_ledger():
    print('******************** QUERY LEDGER ********************')
    query = input("Query:")
    dsvc.query_ledger(query)

def print_ledger():
    print('******************** PRINT LEDGER ********************')
    items_json = dsvc.query_ledger("").to_json()

    data = pd.io.json.json_normalize(json.loads(items_json))
    print(f"# of items {len(data)}")
    with pd.option_context('display.max_columns', 2000, 'display.width', 250):
        print(data)


def clear_ledger():
    print('******************** CLEAR LEDGER ********************')
    dsvc.clear_ledger()
    print("Ledger Cleared\n")

def exit_app():
    print('******************** EXIT APP ********************')
    print ("Goodbye!!")
    time.sleep(1)
    raise KeyboardInterrupt()

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
