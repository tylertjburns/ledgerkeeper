from userInteraction.abstracts.financeInteraction import FinanceInteraction
from userInteraction.cli.cliInteractionManager import  CliInteractionManager
import ledgerkeeper.mongoData.account_data_service as dsvca
import ledgerkeeper.mongoData.ledger_data_service as dsvcl
import ledgerkeeper.mongoData.transaction_data_service as dsvct
from ledgerkeeper.mongoData.transaction import Transaction

from ledgerkeeper.mongoData.account import Account
from ledgerkeeper.enums import PaymentType, AccountType, SpendCategory, TransactionTypes, TransactionSplitType
from enums import CollectionType

class FinanceCliInteraction(FinanceInteraction, CliInteractionManager):

    # region Account UI
    def request_bank_total(self):
        return self.uns.request_float("Current Bank Total: ")

    def select_account(self, statusList=None):
        accountName = self.request_from_dict(dsvca.accounts_as_dict(statusList=statusList))
        if accountName is None:
            return None
        return dsvca.account_by_name(accountName)

    def select_collection(self):
        return self.uns.request_enum(CollectionType)

    def get_record_expense_input(self, accountManager):
        ret = {}
        ret['description'] = self.request_string("Description:")
        ret['debit'] = self.request_float("Debit:")
        ret['payment_type'] = self.request_enum(PaymentType)
        ret['date_stamp'] = self.request_date()

        from_account_name = self.request_from_dict(dsvca.accounts_as_dict(), prompt="From Account:")
        ret['from_account'] = dsvca.account_by_name(from_account_name)
        accountManager.print_positive_remaining(account=ret['from_account'], amount_threshold=ret['debit'])
        eligible_buckets = accountManager.positive_remaining_buckets(account=ret['from_account'],
                                                                     amount_threshold=ret['debit'])
        if eligible_buckets is None or len(eligible_buckets) == 0:
            self.notify_user(f"No eligible Buckets to cover {ret['debit']}")
            return None

        eligible_bucket_names_as_dict = {index: row["name"] for index, row in eligible_buckets.iterrows()}
        from_bucket_name = self.request_from_dict(eligible_bucket_names_as_dict,
                                                 "From Bucket:")
        ret['from_bucket'] = dsvca.bucket_by_account_and_name(ret['from_account'], from_bucket_name)

        return ret

    def get_add_new_account_input(self):
        ret = {}
        ret['account_type'] = self.request_enum(AccountType)
        ret['account_name'] = self.request_string("Account Name:")
        ret['description'] = self.request_string("Description:")

        return ret

    def get_add_bucket_to_account_input(self):
        ret={}
        ret['name'] = self.request_string("Bucket Name: ")
        ret['priority'] = self.request_int("Priority: "),
        ret['due_day'] = self.request_int("Due day of month:"),
        ret['category'] = self.request_enum(SpendCategory)
        ret['base_budget_amount'] = self.request_float("Base budget amount:")
        ret['percent_of_income_adjustment_amount'] = self.request_float("Percentage of Income Budget Adjustment [0-100]: ")

        return ret


    def get_move_funds_input(self, account: Account):
        ret={}
        fromB = self.uns.request_from_dict(dsvca.buckets_as_dict_by_account(account), "Select from bucket:")
        toB = self.uns.request_from_dict(dsvca.buckets_as_dict_by_account(account, set(fromB)), "Select to bucket:")
        amount = self.uns.request_float("Amount to move:", forcePos=True)

        ret['amount'] = amount
        ret['fromBucket'] = dsvca.bucket_by_account_and_name(account, fromB)
        ret['toBucket'] = dsvca.bucket_by_account_and_name(account, toB)

        return ret

    def get_add_waterfall_funds_input(self, account: Account):
        ret = {}
        ret['amount'] = self.request_float("Amount to add:", forcePos=True)
        ret['description'] = self.request_string("Description: ")
        ret['date'] = self.request_date()
        ret['notes'] = self.request_string("Notes: ")
        ret['buckets'] = dsvca.buckets_by_account(account)

        return ret

    def get_delete_bucket_from_account_input(self, account:Account):
        ret={}
        ret['bucketName'] = self.request_from_dict(dsvca.buckets_as_dict_by_account(account), "Bucket:")
        return ret

    def get_update_bucket_priority_input(self, account: Account):
        ret={}
        ret['bucketName'] = self.request_from_dict(dsvca.buckets_as_dict_by_account(account), "Bucket:")
        if ret['bucketName'] is None:
            return None

        currentPrio = dsvca.bucket_by_account_and_name(account, ret['bucketName']).priority

        ret['prior'] = self.request_int(f"Change from {currentPrio} to: ")
        if ret['prior'] is None:
            return None

        return ret

    def get_print_full_waterfall_input(self):
        ret = {}

        ret['bankTotal'] = self.request_float("Bank Total: ")

        return ret

    def get_add_open_balance_input(self):
        ret = {}

        ret['balanceName'] = self.request_string("Balance Name: ")
        ret['balanceValue'] = self.request_float("Pending Amount: ")

        return ret

    def get_delete_open_balance_input(self, account:Account):
        ret = {}

        ret['balanceName'] = self.request_from_dict(dsvca.balances_as_dict_by_account(account), "Balance:")

        return ret

    # endregion

    # region Ledger UI
    def get_add_ledger_manually_input(self):
        ret={}
        ret['description'] = self.request_string("Description:")
        ret['transaction_category'] = self.request_enum(TransactionTypes)
        from_account_name = self.request_from_dict(dsvca.accounts_as_dict(), "From Account:")
        ret['from_account'] = dsvca.account_by_name(from_account_name)

        from_bucket_name = self.request_from_dict(dsvca.buckets_as_dict_by_account(ret['from_account']), "From Bucket:")
        ret['from_bucket'] = dsvca.bucket_by_account_and_name(ret['from_account'], from_bucket_name)

        ret['debit'] = self.request_float("Debit:")
        ret['credit'] = self.request_float("Credit:")

        to_account_name = self.request_from_dict(dsvca.accounts_as_dict(), "To Account:")
        ret['to_account'] = dsvca.account_by_name(to_account_name)

        to_bucket_name = self.request_from_dict(dsvca.buckets_as_dict_by_account(ret['to_account']), "To Bucket:")
        ret['to_bucket'] = dsvca.bucket_by_account_and_name(ret['to_account'], to_bucket_name)
        ret['payment_type'] = self.request_enum(PaymentType)
        ret['date_stamp'] = self.request_date()
        ret['notes'] = self.request_string("Notes:")

        return ret

    def get_split_transaction_input(self, currentAmount:float):

        input = self.request_enum(TransactionSplitType)
        if input == TransactionSplitType.PERCENTAGE:
            perc = self.request_float("% of current to handle [0-100]:")
            amt = max(min(round(currentAmount * perc / 100, 2), currentAmount), 0)
        elif input == TransactionSplitType.DOLLAR:
            amt = max(min(self.request_float(f"Amount to handle [up to {currentAmount}]:"), currentAmount), 0)
        else:
            raise NotImplementedError(f"{input} is not implemented as a TransactionSplitType")

        return amt

    def get_enter_ledger_from_income_transaction_input(self):
        ret = {}
        to_account_name = self.request_from_dict(dsvca.accounts_as_dict(), prompt="To Account:")
        ret['to_account'] = dsvca.account_by_name(to_account_name)

        to_bucket_name = self.request_from_dict(dsvca.buckets_as_dict_by_account(dsvca.account_by_name(ret['to_account'] )),
                                               "To Bucket:")
        ret['to_bucket'] = dsvca.bucket_by_account_and_name(ret['to_account'], to_bucket_name)
        ret['notes'] = self.uns.request_string("Notes:")
        return ret

    def get_enter_ledger_from_expense_transaction_input(self):
        ret= {}
        from_account_name = self.request_from_dict(dsvca.accounts_as_dict(), prompt="From Account:")
        ret['from_account'] = dsvca.account_by_name(from_account_name)
        from_bucket_name = self.request_from_dict(dsvca.buckets_as_dict_by_account(ret['from_account']),
                                                 "From Bucket:")
        ret['from_bucket'] = dsvca.bucket_by_account_and_name(ret['from_account'], from_bucket_name)

        return ret
    # endregion