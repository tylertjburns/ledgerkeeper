import ledgerkeeper.mongoData.account_data_service as dsvca
import ledgerkeeper.mongoData.ledger_data_service as dsvcl
from ledgerkeeper.mongoData.account import Account
from ledgerkeeper.enums import SpendCategory, AccountType, TransactionTypes, AccountStatus, DefaultBuckets, TransactionSource
from enums import ReportType, CollectionType
from userInteraction.abstracts.userInteractionManager import UserIteractionManager
import mongoHelper


class AccountManager():
    def __init__(self, user_notification_system: UserIteractionManager):
        self.uns = user_notification_system


    def delete_account(self):
        name = self.uns.request_from_dict(dsvca.accounts_as_dict(), "Account Name:")

        if name is None:
            return

        yousure = self.uns.request_from_dict({1: "Yes", 2: "No"}, "Are you sure? This will break all reference to this account!")

        if yousure == "Yes":
            account = dsvca.account_by_name(name)
            buckets = dsvca.buckets_by_account(account)

            waterfall_amt = 0
            saved_amt = 0
            for bucket in buckets:
                waterfall_amt += bucket.waterfall_amount
                saved_amt += bucket.saved_amount

            okay_to_delete = False
            if((waterfall_amt > 0) or (saved_amt > 0)):
                response = self.uns.request_from_dict({1: "Yes", 2: "No"}, "Funds in account. Are you sure?")
                if response == "Yes":
                    okay_to_delete = True
            else:
                okay_to_delete = True

            if okay_to_delete:
                dsvca.delete_account(name)
                self.uns.notify_user(f"Account {name} Deleted")
            else:
                self.uns.notify_user(f"Deletion Cancelled.")

    def inactivate_account(self):
        name = self.uns.request_from_dict(dsvca.accounts_as_dict([AccountStatus.ACTIVE.name]), "Account Name:")

        if name is None:
            return

        inactive = dsvca.inactivate_account(dsvca.account_by_name(name))

        if inactive is not None:
            self.uns.notify_user(f"Account {name} Deactivated!")

    def add_new_account(self):
        type = self.uns.request_enum(AccountType)
        name = self.uns.request_string("Account Name:")
        description = self.uns.request_string("Description:")

        account = dsvca.enter_account_if_not_exists(name=name, type=type, description=description)

        if account is not None:
            for e in DefaultBuckets:
                if e in [DefaultBuckets._DEFAULT, DefaultBuckets._OTHER, DefaultBuckets._TAX_WITHOLDING]:
                    spendCat = SpendCategory.OTHER
                elif e in [DefaultBuckets._CREDIT, DefaultBuckets._PAY_WITH_REIMBURSEMENT]:
                    spendCat = SpendCategory.NA
                else:
                    raise NotImplementedError("Unhandled default bucket")
                dsvca.add_bucket_to_account(account, e.name, 99, 99, spendCat)

            self.uns.notify_user("Account created successfully!")
        else:
            self.uns.notify_user(f"Error creating account. An account with the name {name} already exists.")

    def add_bucket_to_account(self):
        account = self.uns.request_from_dict(dsvca.accounts_as_dict([AccountStatus.ACTIVE.name]), prompt="Select an account:")
        name = self.uns.request_string("Bucket Name:")
        prio = self.uns.request_int("Priority:")
        due_day = self.uns.request_int("Due day of month:")
        category = self.uns.request_enum(SpendCategory)
        base_budget_amount = self.uns.request_float("Base budget amount:")
        percent_of_income_adjustment_amount = self.uns.request_float("Percentage of Income Budget Adjustment [0-100]: ")

        bucket = dsvca.add_bucket_to_account(dsvca.account_by_name(account_name=account)
                                             , name=name
                                             , priority=prio
                                             , due_day_of_month=due_day
                                             , spend_category=category
                                             , base_budget_amount=base_budget_amount
                                             , percent_of_income_adjustment_amount=percent_of_income_adjustment_amount
                                             )
        self.uns.notify_user(f"Bucket {bucket.name} added to {account} successfully.")

    def print_buckets(self, accountName=None):
        if accountName is None:
            accountName = self.uns.request_from_dict(dsvca.accounts_as_dict())

        account = dsvca.account_by_name(accountName)
        buckets = dsvca.buckets_by_account(account)
        self.uns.pretty_print_items(sorted(buckets, key=lambda x: x.priority),
                                    title=CollectionType.BUCKETS.name)

    def print_accounts(self):
        self.uns.pretty_print_items(dsvca.query_account("").to_json(), title=CollectionType.ACCOUNTS.name)

    def move_funds(self):
        accountName = self.uns.request_from_dict(dsvca.accounts_as_dict([AccountStatus.ACTIVE.name]), "Select Account:")
        account = dsvca.account_by_name(accountName)
        fromB = self.uns.request_from_dict(dsvca.buckets_as_dict_by_account(account), "Select from bucket:")
        toB = self.uns.request_from_dict(dsvca.buckets_as_dict_by_account(account, set(fromB)), "Select to bucket:")
        amount = self.uns.request_float("Amount to move:", forcePos=True)

        fromBucket = dsvca.bucket_by_account_and_name(account, fromB)
        toBucket = dsvca.bucket_by_account_and_name(account, toB)

        dsvca.update_bucket_saved_amount(account, fromB, fromBucket.saved_amount - amount)
        dsvca.update_bucket_saved_amount(account, toB, toBucket.saved_amount + amount)

    def add_waterfall_funds(self):
        accountName = self.uns.request_from_dict(dsvca.accounts_as_dict([AccountStatus.ACTIVE.name]), "Account:")
        account = dsvca.account_by_name(accountName)
        amount = self.uns.request_float("Amount to add:", forcePos=True)
        description = self.uns.request_string("Description: ")
        date = self.uns.request_date()
        notes = self.uns.request_string("Notes: ")
        buckets = dsvca.buckets_by_account(account)

        ''' Record funds into default account'''
        dsvcl.enter_ledger_entry("NA",
                                 description=description,
                                 transaction_category=TransactionTypes.APPLY_INCOME,
                                 debit=0,
                                 credit=amount,
                                 from_account=description,
                                 from_bucket="income_source",
                                 to_account=accountName,
                                 to_bucket=DefaultBuckets._DEFAULT.name,
                                 spend_category=SpendCategory.NA,
                                 date_stamp=date,
                                 notes=notes,
                                 source=TransactionSource.MANUALENTRY)


        ''' Obtain a sortable list of keys that will be used for iterating through the waterfall'''
        iterSeq = sorted(list(bucket for bucket in buckets), key=lambda x: x.priority)

        ''' Iterate through the keys '''
        excess = amount
        keepExcess = False

        for bucket in iterSeq:
            adjustment = round(bucket.percent_of_income_adjustment_amount / 100.0 * amount, 2)
            dsvca.update_bucket_percentage_budget_amount(account, bucket.name, bucket.perc_budget_amount + adjustment)

            if (excess == 0):
                break

            if (bucket.name == DefaultBuckets._DEFAULT.name):
                keepExcess = True

            excess = self._apply_waterfall_amount_to_bucket(account, bucket, excess, date, keepExcess=keepExcess)

        self.print_buckets(accountName=accountName)
        self.uns.notify_user(f"Amount: {amount} applied successfully")

    def _apply_waterfall_amount_to_bucket(self, account, bucket, amount, date, keepExcess=False):
        if (amount < 0):
            raise Exception(f"Error: Amount must be positive, {amount.amount} was entered.")

        dsvca.update_bucket_waterfall_amount(account, bucket.name, bucket.waterfall_amount + amount)

        waterfall_amount = bucket.waterfall_amount
        waterfall_amount += amount

        total_budget = bucket.base_budget_amount + bucket.perc_budget_amount
        if (bucket.waterfall_amount + amount > total_budget and not (keepExcess)):
            excess = bucket.waterfall_amount + amount - total_budget
            applied_amt = total_budget - bucket.waterfall_amount
        else:
            applied_amt = amount
            excess = 0.0

        dsvca.update_bucket_waterfall_amount(account, bucket.name, bucket.waterfall_amount + applied_amt)

        if (applied_amt != 0) and (bucket.name != DefaultBuckets._DEFAULT.name):
            ''' Move funds from default bucket to waterfall bucket'''
            dsvcl.enter_ledger_entry("NA",
                                     description="Apply from waterfall",
                                     transaction_category=TransactionTypes.MOVE_FUNDS,
                                     debit=applied_amt,
                                     credit=applied_amt,
                                     from_account=account.account_name,
                                     from_bucket=DefaultBuckets._DEFAULT.name,
                                     to_account=account.account_name,
                                     to_bucket=bucket.name,
                                     spend_category=SpendCategory.NA,
                                     date_stamp=date,
                                     notes="",
                                     source=TransactionSource.APPLICATION)

        self.uns.notify_user(f"{amount - excess} applied to bucket {bucket.name}", delay_sec=0)
        return excess

    def cycle_waterfall(self):
        accountName = self.uns.request_from_dict(dsvca.accounts_as_dict([AccountStatus.ACTIVE.name]), "Account:")
        account = dsvca.account_by_name(accountName)
        buckets = dsvca.buckets_by_account(account)

        for bucket in buckets:
            self._cycle_bucket(account, bucket)

        self.uns.notify_user(f"{accountName} cycled")


    def _cycle_bucket(self, account, bucket):
        wf = bucket.waterfall_amount
        dsvca.update_bucket_saved_amount(account, bucket.name, bucket.saved_amount + wf)
        dsvca.update_bucket_waterfall_amount(account, bucket.name, 0)
        dsvca.update_bucket_percentage_budget_amount(account, bucket.name, 0)

    def delete_bucket_from_account(self):
        accountName = self.uns.request_from_dict(dsvca.accounts_as_dict([AccountStatus.ACTIVE.name]), prompt="Select an account:")
        bucketName = self.uns.request_from_dict(dsvca.buckets_as_dict_by_account(dsvca.account_by_name(accountName), ), "Bucket:")

        account = dsvca.account_by_name(accountName)
        bucket = dsvca.delete_bucket_from_account(account, bucketName)

        self.uns.notify_user(f"Bucket {bucket.name} deleted from {account} successfully.")

    def udpate_bucket_priority(self):
        accountName = self.uns.request_from_dict(dsvca.accounts_as_dict([AccountStatus.ACTIVE.name]), prompt="Select an account:")
        bucketName = self.uns.request_from_dict(dsvca.buckets_as_dict_by_account(dsvca.account_by_name(accountName), ), "Bucket:")
        account = dsvca.account_by_name(accountName)

        prior = self.uns.request_int("New Priority: ")

        bucket = dsvca.update_bucket_priority(account, bucketName, prior)

        if bucket is not None:
            self.uns.notify_user(f"{bucketName} priority updated to {prior}")

    def print_full_waterfall(self):
        accountName = self.uns.request_from_dict(dsvca.accounts_as_dict())
        account = dsvca.account_by_name(accountName)
        bankTotal = self.uns.request_float("Bank Total: ")

        self.print_waterfall_summary(account)
        self.print_waterfall_buckets(account)
        self.print_balances(accountName=accountName)
        self.check_balance_against_total()

    def print_waterfall_buckets(self, account: Account = None):
        if account is None:
            accountName = self.uns.request_from_dict(dsvca.accounts_as_dict())
            account = dsvca.account_by_name(accountName)

        buckets = dsvca.buckets_by_account(account)
        data = mongoHelper.list_mongo_to_pandas(buckets)
        data.sort_values(by=["priority", 'due_day_of_month'], inplace=True)

        self.uns.pretty_print_items(data)


    def print_waterfall_summary(self, account: Account = None):
        if account is None:
            accountName = self.uns.request_from_dict(dsvca.accounts_as_dict())
            account = dsvca.account_by_name(accountName)

        buckets = dsvca.buckets_by_account(account)
        data = mongoHelper.list_mongo_to_pandas(buckets)

        waterfall_amount = data['waterfall_amount'].sum()
        saved_amount = data['saved_amount'].sum()

        total_saved = waterfall_amount + saved_amount
        self.uns.notify_user(f"----Waterfall Summary----\n"
                             f"Total Balance: {total_saved}\n"
                             f"Saved for next cycle: {saved_amount}", delay_sec=0)


    def add_open_balance(self):
        accountName = self.uns.request_from_dict(dsvca.accounts_as_dict())
        account = dsvca.account_by_name(accountName)

        balanceName = self.uns.request_string("Balance Name: ")
        balanceValue = self.uns.request_float("Pending Amount: ")

        dsvca.add_open_balance_to_account(account, balanceName, balanceValue)

        self.uns.notify_user(f"Balance {balanceName} added to {account} successfully.")

    def delete_open_balance(self):
        accountName = self.uns.request_from_dict(dsvca.accounts_as_dict())
        account = dsvca.account_by_name(accountName)


        balanceName = self.uns.request_from_dict(dsvca.balances_as_dict_by_account(dsvca.account_by_name(accountName), ), "Balance:")

        balance = dsvca.delete_open_balance_from_account(account, balanceName)

        if balance is not None:
            self.uns.notify_user(f"Balance {balanceName} deleted from {account} successfully.")
        else:
            raise Exception(f"Unable to delete balance from account")

    def print_balances(self, accountName=None):
        if accountName is None:
            accountName = self.uns.request_from_dict(dsvca.accounts_as_dict())
        bankTotal = self.uns.request_float("Current Bank Total: ")

        account = dsvca.account_by_name(accountName)
        balances = dsvca.balances_by_account(account)
        self.uns.notify_user(f"Bank Total: {bankTotal}\n"
                             f"Allocated Total: {self.allocated_total(account)}", delay_sec=0)
        self.uns.pretty_print_items(sorted(balances, key=lambda x: x.name),
                                    title=ReportType.OPENBALANCES.name)

        balance_total = self.check_balance_against_total(bankTotal, accountName=accountName)
        self.uns.notify_user(f"Balance: {balance_total}")

    def check_balance_against_total(self, total:float, accountName=None) -> float:
        if accountName is None:
            accountName = self.uns.request_from_dict(dsvca.accounts_as_dict())

        account = dsvca.account_by_name(accountName)
        balances = dsvca.balances_by_account(account)

        waterfall_saved_total = self.allocated_total(account)
        balance_total = sum(b.amount for b in balances)

        return total + balance_total - waterfall_saved_total

    def allocated_total(self, account: Account):
        buckets = dsvca.buckets_by_account(account)
        return sum(b.saved_amount + b.waterfall_amount for b in buckets)
if __name__ == "__main__":


    a = AccountManager()
    a.print_waterfall_summary()