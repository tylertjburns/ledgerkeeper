from userInteraction.abstracts.userInteractionManager import UserIteractionManager
from ledgerkeeper.mongoData.account import Account
from abc import ABC, abstractmethod
from ledgerkeeper.interfaces.IAccountDataService import IAccountDataService

class FinanceInteraction(UserIteractionManager, ABC):
    # region Account UI
    @abstractmethod
    def request_bank_total(self):
        pass

    @abstractmethod
    def select_account(self, accountDataService: IAccountDataService, statusList=None):
        pass

    @abstractmethod
    def select_collection(self):
        pass

    @abstractmethod
    def get_add_new_account_input(self):
        pass

    @abstractmethod
    def get_record_expense_input(self, accountManager):
        pass

    @abstractmethod
    def get_add_bucket_to_account_input(self):
        pass

    @abstractmethod
    def get_move_funds_input(self, account:Account):
        pass

    @abstractmethod
    def get_add_waterfall_funds_input(self, account: Account):
        pass

    @abstractmethod
    def get_delete_bucket_from_account_input(self, account:Account):
        pass

    @abstractmethod
    def get_update_bucket_priority_input(self, account:Account):
        pass

    @abstractmethod
    def get_print_full_waterfall_input(self):
        pass

    @abstractmethod
    def get_add_open_balance_input(self):
        pass

    @abstractmethod
    def get_delete_open_balance_input(self, account:Account):
        pass
    # endregion

    # region Ledger UI
    @abstractmethod
    def get_add_ledger_manually_input(self):
        pass

    @abstractmethod
    def get_split_transaction_input(self, currentAmount: float):
        pass

    @abstractmethod
    def get_enter_ledger_from_income_transaction_input(self):
        pass

    @abstractmethod
    def get_enter_ledger_from_expense_transaction_input(self):
        pass
    # endregion