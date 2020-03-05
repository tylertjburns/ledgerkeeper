from mongoData.transaction import Transaction
import mongoData.account_data_service as dsvca

import dataFileTranslation as dft
from enums import TransactionSource, CollectionType, PlotType
import ledgerManager as lm
import accountManager as am
from userInteraction.cli.cliInteractionManager import CliInteractionManager

NOTIMPLEMENTED = "-------------- NOT IMPLEMENTED ----------------"
userInteraction = CliInteractionManager()
ledgerManager = lm.LedgerManager(userInteraction)
accountManager = am.AccountManager(userInteraction)


def request_action():
    print('******************* MAIN MENU **********************')

    print("Which action would you like to take?")
    print("")
    print("[A]dd new ledger entry manually")
    print("Add [N]ew Account")
    print("Add Buc[K]et to account")
    print("Apply [I]ncome")
    print("[L]oad transactions")
    print("P[R]ocess new transactions")
    print("[D]elete")
    print("[Q]uery ledger")
    print("[C]lear Collection")
    print("[P]rint Collection")
    print("Pl[O]t options")
    print("E[X]it")
    return input("").upper()

def action_switch(input: str):
    switcher = {
        "A": add_ledger,
        "C": clear_collection,
        "D": delete_loop,
        "I": apply_income,
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

def delete_switch(input: str):
    switcher = {
        "A": delete_account,
        "B": delete_bucket,
        "L": delete_a_ledger_item,
    }
    return switcher.get(input, None)

def plot_switch(input: str):
    switcher = {
        PlotType.HISTORY_BY_CATEGORY.name: ledgerManager.plot_history_by_category,
        PlotType.PROJECTED_FINANCE.name: ledgerManager.plot_projected_finance,
    }
    return switcher.get(input, None)

def add_new_account():
    print('******************** NEW ACCOUNT *********************')
    accountManager.add_new_account()

def delete_account():
    print('******************** DELETE ACCOUNT *********************')
    accountManager.delete_account()

def add_ledger():
    print('******************** ADD LEDGER **********************')
    ledgerManager.add_ledger()

def query_ledger():
    print('******************** QUERY LEDGER ********************')
    ledgerManager.query_ledger()

def print_collection():
    print('******************** PRINT ***************************')

    print_type = userInteraction.request_enum(CollectionType)

    if CollectionType[print_type] == CollectionType.LEDGER:
        ledgerManager.print_ledger()
    elif CollectionType[print_type] == CollectionType.TRANSACTIONS:
        ledgerManager.print_transactions()
    elif CollectionType[print_type] == CollectionType.BUCKETS:
        accountManager.print_buckets()
    elif CollectionType[print_type] == CollectionType.ACCOUNTS:
        accountManager.print_accounts()
    else:
        raise NotImplementedError(f"No print type setup for {print_type}")

    print("")


def clear_collection():
    print('******************* CLEAR COLLECTION *****************')
    ledgerManager.clear_collection()

def delete_a_ledger_item():
    print('******************* DELETE A LEDGER ITEM *************')
    ledgerManager.delete_a_ledger_item()

def exit_app():
    print('******************** EXIT APP ************************')
    ledgerManager.uns.notify_user("Goodbye!")
    raise KeyboardInterrupt()

def plot_request_loop():
    print('******************** Plotting ***************************')
    while True:
        direction = userInteraction.request_enum(PlotType, "What do you want to plot?")

        if direction is None:
            return

        action = plot_switch(direction)

        if action is None:
            userInteraction.notify_user("Invalid Entry...")
        else:
            action()

def delete_loop():
    print('******************** Deleting ***************************')

    while True:
        print("What do you want to delete?")

        print("[A]ccount")
        print("[B]ucket")
        print("[L]edger")
        print("E[X]it to menu")
        print("")
        inp = input("").upper()

        if inp == "X":
            return

        action = delete_switch(inp)
        if action is not None:
            action()
        else:
            print("Invalid Selection")




def process_transactions_loop():
    print('******************** Process Transaction ***************')
    ledgerManager.process_transactions_loop()

def load_new_transactions():
    print('******************** Load New Transactions *************')

    # Ask User for source
    source = userInteraction.request_enum(TransactionSource)

    # Get Filepath
    in_path = userInteraction.request_filepath()

    # React to user input
    if TransactionSource[source] == TransactionSource.BARCLAYCARDUS:
        transactions = dft.read_in_barclay_transactions(in_path)
    elif TransactionSource[source] == TransactionSource.PNC:
        transactions = dft.read_in_pnc_transactions(in_path)
    elif TransactionSource[source] == TransactionSource.ARCHIVE:
        account = userInteraction.request_from_dict(dsvca.accounts_as_dict())
        transactions = dft.read_in_old_ledgers(filepath=in_path, account=dsvca.account_by_name(account))
        userInteraction.notify_user("Ledger Items created directly")
    else:
        print(NOTIMPLEMENTED)
        return

    userInteraction.notify_user(f"{len(transactions)} new Transactions from {source}")

def add_bucket_to_account():
    print('******************** Add Bucket to Account ********************')
    accountManager.add_bucket_to_account()

def delete_bucket():
    print('******************** Delete Bucket from Account ********************')
    accountManager.delete_bucket_from_account()

def apply_income():
    print('******************** APPLY INCOME ********************')
    accountManager.add_waterfall_funds()

if __name__ == "__main__":
    import mongo_setup
    mongo_setup.global_init()

    while True:
        action = action_switch(request_action())
        if action is not None:
            action()
        else:
            userInteraction.notify_user("Invalid Entry...")
