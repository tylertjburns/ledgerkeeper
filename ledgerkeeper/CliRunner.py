import mongoData.ledger_data_service as dsvcl
from mongoData.transaction import Transaction
import mongoData.transaction_data_service as dsvct
import mongoData.account_data_service as dsvca

import dataFileTranslation as dft
from enums import TransactionSource, TransactionTypes, CollectionType, TransactionStatus, TransactionSplitType, AccountType, SpendCategory
import uuid
import ledgerManager as lm
from userInteraction.cli.cliInteractionManager import CliInteractionManager


# from cliHelper import _notify_user, \
#     _request_filepath,\
#     _request_from_dict, \
#     _request_enum, \
#     _request_float, \
#     _request_int, \
#     _request_date,\
#     _pretty_print_items,\
#     _request_string


NOTIMPLEMENTED = "-------------- NOT IMPLEMENTED ----------------"
cliManager = CliInteractionManager()
ledgerManager = lm.LedgerManager(cliManager)

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

def add_new_account():
    print('******************** NEW ACCOUNT ********************')
    ledgerManager.add_new_account()

def add_ledger():
    print('******************** ADD LEDGER ********************')
    ledgerManager.add_ledger()

def get_new_item():
    print('******************** GET NEW ITEM ********************')
    print(NOTIMPLEMENTED)

def query_ledger():
    print('******************** QUERY LEDGER ********************')
    ledgerManager.query_ledger()

def print_collection():
    print('******************** PRINT ********************')
    ledgerManager.print_collection()


def clear_collection():
    print('******************** CLEAR COLLECTION ********************')
    ledgerManager.clear_collection()

def delete_a_ledger_item():
    print('******************** DELETE A LEDGER ITEM ********************')
    ledgerManager.delete_a_ledger_item()

def exit_app():
    print('******************** EXIT APP ********************')
    ledgerManager.uns.notify_user("Goodbye!")
    raise KeyboardInterrupt()

def process_transaction(transaction: Transaction):
    ledgerManager.process_transaction(transaction)

def plot_request_loop():
    print('******************** Plotting ********************')
    ledgerManager.plot_request_loop()

def process_transactions_loop():
    print('******************** Process Transaction ********************')
    ledgerManager.process_transactions_loop()

def load_new_transactions():
    print('******************** Load New Transactions ********************')

    # Ask User for source
    source = cliManager.request_enum(TransactionSource)

    # Get Filepath
    in_path = cliManager.request_filepath()

    # React to user input
    if TransactionSource[source] == TransactionSource.BARCLAYCARDUS:
        transactions = dft.read_in_barclay_transactions(in_path)
    elif TransactionSource[source] == TransactionSource.PNC:
        transactions = dft.read_in_pnc_transactions(in_path)
    elif TransactionSource[source] == TransactionSource.ARCHIVE:
        account = cliManager.request_from_dict(dsvca.accounts_as_dict())
        transactions = dft.read_in_old_ledgers(filepath=in_path, account=dsvca.account_by_name(account))
        cliManager.notify_user("Ledger Items created directly")
    else:
        print(NOTIMPLEMENTED)

    cliManager.notify_user(f"{len(transactions)} new Transactions from {source}")

def add_bucket_to_account():
    print('******************** Add Bucket to Account ********************')
    ledgerManager.add_bucket_to_account()


if __name__ == "__main__":
    import mongo_setup
    mongo_setup.global_init()

    while True:
        action = action_switch(request_action())
        if action is not None:
            action()
        else:
            cliManager.notify_user("Invalid Entry...")
