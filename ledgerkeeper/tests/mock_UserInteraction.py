
from userInteraction.abstracts.financeInteraction import FinanceInteraction
from ledgerkeeper.interfaces.IAccountDataService import IAccountDataService
from ledgerkeeper.mongoData.account import Account
import datetime
from typing import Dict

class mock_UserInteraction(FinanceInteraction):

    def request_bank_total(self):
        return 100

    def select_account(self, accountDataService: IAccountDataService, statusList=None):
        return Account()

    def select_collection(self):
        return 1

    def get_add_new_account_input(self):
        return {"test": 1}

    def get_record_expense_input(self, accountManager):
        return {"test": 1}

    def get_add_bucket_to_account_input(self):
        return {"test": 1}

    def get_move_funds_input(self, account: Account):
        return {"test": 1}

    def get_add_waterfall_funds_input(self, account: Account):
        return {"test": 1}

    def get_delete_bucket_from_account_input(self, account: Account):
        return {"test": 1}

    def get_update_bucket_priority_input(self, account: Account):
        return {"test": 1}

    def get_print_full_waterfall_input(self):
        return {"test": 1}

    def get_add_open_balance_input(self):
        return {"test": 1}

    def get_delete_open_balance_input(self, account: Account):
        return {"test": 1}

    def get_add_ledger_manually_input(self):
        return {"test": 1}

    def get_split_transaction_input(self, currentAmount: float):
        return {"test": 1}

    def get_enter_ledger_from_income_transaction_input(self):
        return {"test": 1}

    def get_enter_ledger_from_expense_transaction_input(self):
        return {"test": 1}

    def notify_user(self, text: str):
        return True

    def request_string(self, prompt: str):
        return "test"

    def request_int(self, prompt: str):
        return 1

    def request_enum(self, enum):
        return enum[1]

    def request_float(self, prompt: str):
        return 1.0

    def request_guid(self, prompt: str):
        return "GUID"

    def request_date(self):
        return datetime.datetime.today().strftime('%Y-%m-%d')

    def request_from_dict(self, selectionDict: Dict[int, str], prompt=None) -> str:
        return selectionDict[1]

    def request_open_filepath(self):
        return "filepath"

    def request_save_filepath(self):
        return "filepath"

    def request_you_sure(self, items, prompt=None):
        return "Yes"

    def pretty_print_items(self, items, title=None):
        return True