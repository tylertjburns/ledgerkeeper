import ledgerkeeper.mongoData.account_data_service as dsvca
import ledgerkeeper.mongoData.ledger_data_service as dsvcl
import ledgerkeeper.mongoData.transaction_data_service as dsvct
import balancesheet.mongoData.equities_data_service as dsvce

import ledgerkeeper.dataFileTranslation as dft
from ledgerkeeper.enums import TransactionSource
from coreEnums import CollectionType, ReportType, PlotType
import ledgerkeeper.ledgerManager as lm
import ledgerkeeper.accountManager as am
import balancesheet.equityManager as em
import ledgerkeeper.transactionManager as tm
from userInteraction.financeCliInteraction import FinanceCliInteraction

NOTIMPLEMENTED = "-------------- NOT IMPLEMENTED ----------------"
userInteraction = FinanceCliInteraction()
ledgerManager = lm.LedgerManager(userInteraction)
accountManager = am.AccountManager(userInteraction)
equityManager = em.EquityManager(userInteraction)
transactionManager = tm.TransactionManager(userInteraction)

def main():
    loop(main_menu_switch, main_menu)

def ret():
    return

def loop(switch, request):
    while True:
        action = switch(request())
        if action == ret:
            return
        elif action == exit_app:
            action()
            return
        elif action is not None:
            action()
        else:
            userInteraction.notify_user("Invalid Entry...")

def main_menu_switch(input:str):
    switcher = {
        "A": accounts_sub_menu_loop,
        "E": equity_sub_menu_loop,
        "L": ledger_sub_menu_loop,
        "P": print_sub_menu_loop,
        "C": clear_collection,
        'O': plot_request_loop,
        "X": exit_app
    }
    return switcher.get(input, None)

def main_menu():
    print('******************* MAIN MENU **********************')
    print("Select sub-menu")
    print("")
    print("[A]ccounts")
    print("[E]quities")
    print("[L]edger")
    print("[P]rint")
    print("[C]lear collection")
    print("Pl[O]t options")
    print("E[X]it")

    return input("").upper()

def accounts_sub_menu_switch(input:str):
    switcher = {
        "A": add_new_account,
        "B": add_bucket_to_account,
        "C": add_open_balance_to_account,
        "D": delete_account,
        "E": deactivate_account,
        "I": apply_income,
        "K": delete_bucket,
        "M": remove_open_balance_from_account,
        "O": change_bucket_priority,
        "RCSV": update_buckets_from_csv,
        "T": enter_transaction,
        "WCSV": write_buckets_to_csv,
        'Y': cycle_waterfall,
        "X": ret
    }
    return switcher.get(input, None)

def accounts_sub_menu():
    print('******************* ACCOUNTS **********************')
    print("[A]dd new Account")
    print("[D]elete Account")
    print("D[E]activate Account")
    print("Apply [I]ncome")
    print("Enter [T]ransaction")
    print("Add [B]ucket to account")
    print("Delete Buc[K]et")
    print("[WCSV] Write buckets to CSV")
    print("[RCSV] Update buckets from CSV")
    print("C[Y]cle Waterfall")
    print("Change Pri[O]rity")
    print("Add open balan[C]e to account")
    print("Re[M]ove open balance from account")
    print("[X] Back")

    return input("").upper()

def accounts_sub_menu_loop():
    loop(accounts_sub_menu_switch, accounts_sub_menu)

def ledger_sub_menu_switch(input: str):
    switcher = {
        "A": add_ledger,
        "L": load_new_transactions,
        'R': process_transactions_loop,
        "Q": query_ledger,
        "X": ret
    }
    return switcher.get(input, None)

def ledger_sub_menu():
    print('******************* LEDGER **********************')
    print("[A]dd new ledger entry manually")
    print("[L]oad transactions")
    print("P[R]ocess new transactions")
    print("[Q]uery ledger")
    print("[X] Back")

    return input("").upper()

def ledger_sub_menu_loop():
    loop(ledger_sub_menu_switch, ledger_sub_menu)


def print_sub_menu_switch(input: str):
    switcher = {
        "C": print_collection,
        "R": print_report,
        "X": ret
    }
    return switcher.get(input, None)

def print_sub_menu():
    print('******************* PRINT **********************')
    print("[C]ollection")
    print("[R]eport")
    print("[X] Back")

    return input("").upper()

def print_sub_menu_loop():
    loop(print_sub_menu_switch, print_sub_menu)

def equity_sub_menu_switch(input: str):
    switcher = {
        "A": add_equity,
        "D": delete_equity,
        'R': record_equity_value_snapshot,
        "X": ret
    }
    return switcher.get(input, None)

def equity_sub_menu():
    print('******************* EQUITIES **********************')
    print("[A]dd new equity")
    print("[D]elete equity")
    print("[R]ecord new value snapshot")
    print("[X] Back")

    return input("").upper()

def equity_sub_menu_loop():
    loop(equity_sub_menu_switch, equity_sub_menu)

def plot_switch(input: PlotType):
    switcher = {
        PlotType.HISTORY_BY_CATEGORY: accountManager.plot_history_by_category,
        PlotType.PROJECTED_FINANCE: accountManager.plot_projected_finance,
        PlotType.ASSET_LIABILITY_NET_OVER_TIME: equityManager.plot_balance_over_time,
        None: ret
    }
    return switcher.get(input, None)

def plot_sub_menu():
    print('******************** Plotting ***************************')
    return userInteraction.request_enum(PlotType, "What do you want to plot?")

def plot_request_loop():
    loop(plot_switch, plot_sub_menu)

def add_new_account():
    print('******************** NEW ACCOUNT *********************')
    accountManager.add_new_account()

def delete_account():
    print('******************** DELETE ACCOUNT *********************')
    accountManager.delete_account(ledgerManager)

def add_ledger():
    print('******************** ADD LEDGER **********************')
    ledgerManager.add_ledger_manually()

def query_ledger():
    print('******************** QUERY LEDGER ********************')
    ledgerManager.query_ledger()

def print_collection():
    print('******************** PRINT COLLECTION ***************************')

    print_type = userInteraction.request_enum(CollectionType)
    if print_type is None:
        return

    if print_type == CollectionType.LEDGER:
        ledgerManager.print_ledger()
    elif print_type == CollectionType.TRANSACTIONS:
        transactionManager.print_transactions()
    elif print_type == CollectionType.BUCKETS:
        accountManager.print_buckets()
    elif print_type == CollectionType.ACCOUNTS:
        accountManager.print_accounts()
    elif print_type == CollectionType.ENTITIES:
        equityManager.print_equities()
    elif print_type == CollectionType.ENTITY_VALUE_SNAPSHOTS:
        equityManager.print_value_snapshots()
    else:
        raise NotImplementedError(f"No print type setup for {print_type}")

    print("")

def print_report():
    print('******************** PRINT REPORT ***************************')

    print_type = userInteraction.request_enum(ReportType)
    if print_type is None:
        return

    if print_type == ReportType.BALANCESHEETOVERTIME:
        equityManager.print_balance_sheet()
    elif print_type == ReportType.WATERFALLSUMMARY:
        accountManager.print_waterfall_summary()
    elif print_type == ReportType.FULLWATERFALL:
        accountManager.print_full_waterfall()
    elif print_type == ReportType.OPENBALANCES:
        accountManager.print_balances()
    elif print_type == ReportType.BUCKETSPOSITIVEREMAINING:
        accountManager.print_positive_remaining()
    else:
        raise NotImplementedError(f"No print type setup for {print_type.name}")

    print("")

def clear_collection():
    print('******************* CLEAR COLLECTION *****************')
    collection = userInteraction.request_enum(CollectionType)

    if collection is None:
        return

    if collection == CollectionType.LEDGER:
        dsvcl.clear_ledger()
    elif collection == CollectionType.TRANSACTIONS:
        dsvct.clear_collection()
    elif collection == CollectionType.ENTITIES:
        dsvce.clear_equities()
    else:
        userInteraction.notify_user(f"Undefined collection for clearing {collection}")
        return

    userInteraction.notify_user(f"{collection} collection cleared\n")


def delete_a_ledger_item():
    print('******************* DELETE A LEDGER ITEM *************')
    ledgerManager.delete_a_ledger_item()

def exit_app():
    print('******************** EXIT APP ************************')
    ledgerManager.uns.notify_user("Goodbye!")

def process_transactions_loop():
    print('******************** Process Transaction ***************')
    transactionManager.process_transactions_loop()

def load_new_transactions():
    print('******************** Load New Transactions *************')

    # Ask User for source
    source = userInteraction.request_from_dict({
        1: TransactionSource.PNC.name,
        2: TransactionSource.BARCLAYCARDUS.name,
        3: TransactionSource.ARCHIVE.name
    }
    )

    if source is None:
        return

    # Get Filepath
    in_path = userInteraction.request_open_filepath()

    # React to user input
    if source == TransactionSource.BARCLAYCARDUS.name:
        transactions = dft.read_in_barclay_transactions(in_path)
    elif source == TransactionSource.PNC.name:
        transactions = dft.read_in_pnc_transactions(in_path)
    elif source == TransactionSource.ARCHIVE.name:
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

def cycle_waterfall():
    print('******************** CYCLE WATERFALL ********************')
    accountManager.cycle_waterfall()

def add_equity():
    print('******************** ADD EQUITY ********************')
    equityManager.add_equity()

def delete_equity():
    print('******************** DELETE EQUITY ********************')
    equityManager.delete_equity()

def record_equity_value_snapshot():
    print('******************** RECORD EQUITY VALUE ********************')
    equityManager.record_value()

def deactivate_account():
    print('******************** DEACTIVATE ACCOUNT ********************')
    accountManager.inactivate_account()

def change_bucket_priority():
    print('******************** CHANGE PRIORITY ********************')
    accountManager.udpate_bucket_priority()

def add_open_balance_to_account():
    print('******************** ADD OPEN BALANCE ********************')
    accountManager.add_open_balance()

def remove_open_balance_from_account():
    print('******************** REMOVE OPEN BALANCE ********************')
    accountManager.delete_open_balance()

def update_buckets_from_csv():
    print('******************** BUCKETS FROM CSV ********************')
    accountManager.buckets_from_csv()

def write_buckets_to_csv():
    print('******************** BUCKETS TO CSV ********************')
    accountManager.save_buckets_as_csv()

def enter_transaction():
    print('******************** RECORD EXPENSE ********************')
    accountManager.enter_manual_transaction(ledgerManager)

if __name__ == "__main__":
    import logging
    import loggingConfig
    import mongo_setup

    loggingConfig.initLogging(loggingLvl=logging.DEBUG)
    mongo_setup.global_init()

    main()
