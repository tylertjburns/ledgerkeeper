import ledgerkeeper.mongoData.account_data_service as dsvca
import ledgerkeeper.mongoData.ledger_data_service as dsvcl
import ledgerkeeper.mongoData.transaction_data_service as dsvct
from ledgerkeeper.mongoData.account import Account
from ledgerkeeper.enums import SpendCategory, AccountType, TransactionTypes, AccountStatus, DefaultBuckets, TransactionSource, PaymentType, TransactionStatus, PaymentMethod
from coreEnums import ReportType, CollectionType
from userInteraction.financeCliInteraction import FinanceCliInteraction
import mongoHelper
import pandas as pd
import uuid
from sessionState import SessionState
import plotter as plt
import logging

class AccountManager():
    def __init__(self, user_interaction_system: FinanceCliInteraction):
        self.uns = user_interaction_system
        self.state = SessionState()

    def enter_manual_transaction(self, ledgerManager):
        swticher = {
            TransactionTypes.APPLY_INCOME: self._apply_income,
            TransactionTypes.BALANCE_BANK: self._balance_bank,
            TransactionTypes.RECORD_EXPENSE: self._record_expense,
            TransactionTypes.RECEIVE_REFUND: self._receive_refund
        }

        transaction_category = self.uns.request_enum(TransactionTypes)

        action = swticher.get(transaction_category, None)

        if action is not None:
            action()
        else:
            raise NotImplementedError(f"Unhandled Transaction Type: {transaction_category}")

    def _apply_income(self):
        self.uns.notify_user("Not Implemented")

    def _balance_bank(self):
        self.uns.notify_user("Not Implemented")

    def _record_expense(self):
        trans_id = str(uuid.uuid4())

        input = self.uns.get_record_expense_input(self)
        if input is None:
            return

        from_account = input['from_account']
        from_bucket = input['from_bucket']

        transaction = dsvct.enter_if_not_exists(
            transaction_id=trans_id,
            description=input["description"],
            transaction_category=TransactionTypes.RECORD_EXPENSE,
            debit=input['debit'],
            credit=0,
            source=TransactionSource.MANUALENTRY,
            payment_type=input['payment_type'],
            date_stamp=input['date_stamp'],
            handled=TransactionStatus.UNHANDLED
        )

        ledger = ledgerManager.approve_transaction(transaction, self)
        dsvca.update_bucket_saved_amount(account=from_account, bucketName=ledger.from_bucket, newAmount=from_bucket.saved_amount - input['debit'])

        # Need to add an open balance if the payment type was Bank
        if input['payment_type'] == PaymentType.BANK:
            dsvca.add_open_balance_to_account(from_account, input['description'], input['debit'])


    def _receive_refund(self, ledgerManager):
        self.uns.notify_user("Not Implemented")


    def delete_account(self, ledgerManager, account:Account=None):
        account = account if account else self.uns.select_account()
        if account is None:
            return

        yousure = self.uns.request_you_sure("Are you sure? This will break all reference to this account!")
        if yousure is None:
            return

        if yousure == "Yes":
            buckets = dsvca.buckets_by_account(account)

            waterfall_amt = 0
            saved_amt = 0
            for bucket in buckets:
                waterfall_amt += bucket.waterfall_amount
                saved_amt += bucket.saved_amount

            okay_to_delete = False
            if((waterfall_amt > 0) or (saved_amt > 0)):
                yousure = self.uns.request_you_sure("Funds in account. Are you sure?")
                if yousure is None:
                    return

                if yousure == "Yes":
                    okay_to_delete = True
            else:
                okay_to_delete = True

            if okay_to_delete:
                dsvca.delete_account(account.account_name)
                self.uns.notify_user(f"Account {account.account_name} Deleted")
            else:
                self.uns.notify_user(f"Deletion Cancelled.")

    def inactivate_account(self, account:Account=None):
        account = account if account else self.uns.select_account()

        inactive = dsvca.inactivate_account(account=account)

        if inactive is not None:
            self.uns.notify_user(f"Account {account.account_name} Deactivated!")

    def add_new_account(self) -> Account:
        input = self.uns.get_add_new_account_input()
        if input is None:
            return None

        account = dsvca.enter_account_if_not_exists(name=input['account_name'], type=input['account_type'], description=input['description'])

        if account is not None:
            for e in DefaultBuckets:
                if e in [DefaultBuckets._DEFAULT, DefaultBuckets._OTHER, DefaultBuckets._TAX_WITHOLDING]:
                    spendCat = SpendCategory.OTHER
                elif e in [DefaultBuckets._CREDIT, DefaultBuckets._PAY_WITH_REIMBURSEMENT]:
                    spendCat = SpendCategory.NOTAPPLICABLE
                else:
                    raise NotImplementedError("Unhandled default bucket")
                dsvca.add_bucket_to_account(account, e.name, 99, 99, spendCat)

            self.uns.notify_user("Account created successfully!")
        else:
            self.uns.notify_user(f"Error creating account. An account with the name {input['account_name']} already exists.")

        return account

    def add_bucket_to_account(self, account:Account=None):
        account = account if account else self.uns.select_account()

        input = self.uns.get_add_bucket_to_account_input()

        if input is None:
            return

        bucket = dsvca.add_bucket_to_account(account=account
                                             , name=input['bucket_name']
                                             , priority=input['bucket_priority']
                                             , due_day_of_month=input['bucket_due_day']
                                             , spend_category=input['bucket_category']
                                             , base_budget_amount=input['bucket_base_budget_amount']
                                             , percent_of_income_adjustment_amount=input['bucket_percent_of_income_adjustment_amount']
                                             )
        self.uns.notify_user(f"Bucket {bucket.name} added to {account.account_name} successfully.")

    def print_buckets(self, account:Account=None):
        account = account if account else self.uns.select_account()
        buckets = dsvca.buckets_by_account(account)
        self.uns.notify_user("\n------Buckets------", delay_sec=0)
        self.uns.pretty_print_items(sorted(buckets, key=lambda x: x.priority),
                                    title=CollectionType.BUCKETS.name)

    def print_accounts(self):
        self.uns.pretty_print_items(dsvca.query_account("").to_json(), title=CollectionType.ACCOUNTS.name)

    def move_funds(self, account:Account=None):
        account = account if account else self.uns.select_account()
        input = self.uns.get_move_funds_input(account)
        if input is None:
            return

        dsvca.update_bucket_saved_amount(account, input['fromBucket'].name, input['fromBucket'].saved_amount - input['amount'])
        dsvca.update_bucket_saved_amount(account, input['toBucket'].name, input['toBucket'].saved_amount + input['amount'])

    def add_waterfall_funds(self, account:Account=None):
        account = account if account else self.uns.select_account()
        input = self.uns.get_add_waterfall_funds_input(account=account)

        ''' Record funds into default account'''
        dsvcl.enter_ledger_entry("NA",
                                 description=input['description'],
                                 transaction_category=TransactionTypes.APPLY_INCOME,
                                 debit=0,
                                 credit=input['amount'],
                                 from_account=input['description'],
                                 from_bucket="income_source",
                                 to_account=account.account_name,
                                 to_bucket=DefaultBuckets._DEFAULT.name,
                                 spend_category=SpendCategory.NOTAPPLICABLE,
                                 date_stamp=input['date'],
                                 notes=input['notes'],
                                 source=TransactionSource.MANUALENTRY,
                                 payment_type=PaymentType.NOTAPPLICABLE)


        ''' Obtain a sortable list of keys that will be used for iterating through the waterfall'''
        iterSeq = sorted(list(bucket for bucket in input['buckets']), key=lambda x: x.priority)

        ''' Iterate through the keys '''
        excess = input['amount']
        keepExcess = False

        for bucket in iterSeq:
            adjustment = round(bucket.percent_of_income_adjustment_amount / 100.0 * input['amount'], 2)
            dsvca.update_bucket_percentage_budget_amount(account, bucket.name, bucket.perc_budget_amount + adjustment)

            if (excess == 0):
                break

            if (bucket.name == DefaultBuckets._DEFAULT.name):
                keepExcess = True

            excess = self._apply_waterfall_amount_to_bucket(account, bucket, excess, input['date'], keepExcess=keepExcess)

        self.print_buckets(account=account)
        self.uns.notify_user(f"Amount: {input['amount']} applied successfully")

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
                                     spend_category=SpendCategory.NOTAPPLICABLE,
                                     date_stamp=date,
                                     notes="",
                                     source=TransactionSource.APPLICATION,
                                     payment_type=PaymentType.NOTAPPLICABLE)

        self.uns.notify_user(f"{amount - excess} applied to bucket {bucket.name}", delay_sec=0)
        return excess

    def cycle_waterfall(self, account:Account=None):
        account = account if account else self.uns.select_account()
        buckets = dsvca.buckets_by_account(account)

        for bucket in buckets:
            self._cycle_bucket(account, bucket)

        self.uns.notify_user(f"{account.account_name} cycled")


    def _cycle_bucket(self, account, bucket):
        wf = bucket.waterfall_amount
        dsvca.update_bucket_saved_amount(account, bucket.name, bucket.saved_amount + wf)
        dsvca.update_bucket_waterfall_amount(account, bucket.name, 0)
        dsvca.update_bucket_percentage_budget_amount(account, bucket.name, 0)

    def delete_bucket_from_account(self, account:Account=None):
        account = account if account else self.uns.select_account()
        input = self.uns.get_delete_bucket_from_account_input(account)

        ret = dsvca.delete_bucket_from_account(account, input['bucketName'])

        if ret == 1:
            self.uns.notify_user(f"Bucket {input['bucketName']} deleted from {account} successfully.")
        else:
            self.uns.notify_user(f"Error deleting bucket {input['bucketName']} from {account}.")

    def udpate_bucket_priority(self, account:Account=None):
        account = account if account else self.uns.select_account()
        input = self.uns.get_update_bucket_priority_input(account)
        if input is None:
            return None

        bucket = dsvca.update_bucket_priority(account, input['bucketName'], input['prior'])

        if bucket is not None:
            self.uns.notify_user(f"{input['bucketName']} priority updated to {input['prior']}")

    def print_full_waterfall(self, account:Account=None):
        account = account if account else self.uns.select_account()

        input = self.uns.get_print_full_waterfall_input()

        self.print_waterfall_summary(account)
        self.print_positive_remaining(account)
        self.print_balances(bankTotal=input['bankTotal'], account=account)
        self.check_balance_against_total(input['bankTotal'], account=account)

    def print_waterfall_buckets(self, account: Account = None):
        account = account if account else self.uns.select_account()

        buckets = dsvca.buckets_by_account(account)
        data = mongoHelper.list_mongo_to_pandas(buckets)
        data.sort_values(by=["priority", 'due_day_of_month'], inplace=True)

        self.uns.pretty_print_items(data)


    def print_waterfall_summary(self, account: Account = None):
        account = account if account else self.uns.select_account()

        buckets = dsvca.buckets_by_account(account)
        data = mongoHelper.list_mongo_to_pandas(buckets)

        waterfall_amount = data['waterfall_amount'].sum()
        saved_amount = data['saved_amount'].sum()

        total_saved = waterfall_amount + saved_amount
        self.uns.notify_user(f"\n------Waterfall Summary------\n"
                             f"Total Balance: ${round(total_saved, 2)}\n"
                             f"Saved for next cycle: S{round(saved_amount, 2)}", delay_sec=0)


    def add_open_balance(self, account:Account=None):
        account = account if account else self.uns.select_account()
        input = self.uns.get_add_open_balance_input()
        dsvca.add_open_balance_to_account(account, input['balanceName'], input['balanceValue'])
        self.uns.notify_user(f"Balance {input['balanceName']} added to {account} successfully.")

    def delete_open_balance(self, account:Account=None):
        account = account if account else self.uns.select_account()
        input = self.uns.get_delete_open_balance_input(account)

        balance = dsvca.delete_open_balance_from_account(account, input['balanceName'])

        if balance is not None:
            self.uns.notify_user(f"Balance {input['balanceName']} deleted from {account} successfully.")
        else:
            raise Exception(f"Unable to delete balance from account")

    def print_balances(self, bankTotal: float = None, account:Account=None):
        account = account if account else self.uns.select_account()

        if bankTotal is None:
            bankTotal = self.uns.request_bank_total()

        balances = dsvca.balances_by_account(account)
        self.uns.notify_user(f"\n------Balances------\n"
                             f"Bank Total: {self.float_as_currency(bankTotal)}\n"
                             f"Allocated Total: {self.float_as_currency(self.allocated_total(account))}", delay_sec=0)
        self.uns.pretty_print_items(sorted(balances, key=lambda x: x.name),
                                    title=ReportType.OPENBALANCES.name)

        balance_total = self.check_balance_against_total(bankTotal, account=account)
        self.uns.notify_user(f"------------------------\n"
                             f"Balance: {self.float_as_currency(balance_total)}")

    def check_balance_against_total(self, total: float, account:Account=None) -> float:
        account = account if account else self.uns.select_account()

        balances = dsvca.balances_by_account(account)

        waterfall_saved_total = self.allocated_total(account)
        balance_total = sum(b.amount for b in balances)

        return total + balance_total - waterfall_saved_total

    def allocated_total(self, account: Account):
        buckets = dsvca.buckets_by_account(account)
        return sum(b.saved_amount + b.waterfall_amount for b in buckets)

    def save_buckets_as_csv(self, account: Account = None):
        account = account if account else self.uns.select_account()

        buckets = dsvca.buckets_by_account(account)
        data = mongoHelper.list_mongo_to_pandas(buckets)

        filepath = self.uns.request_save_filepath()

        data.to_csv(filepath)
        if data is None:
            return

        self.uns.notify_user(f"Buckets data written successfully to {filepath}")

    def buckets_from_csv(self, account: Account = None):
        account = account if account else self.uns.select_account()

        self.uns.notify_user(f"Please select a .csv file containing the columns:"
                             f"\n\tpriority"
                             f"\n\tname"
                             f"\n\tprovider"
                             f"\n\tpayment_account"
                             f"\n\tpayment_method"
                             f"\n\tdue_day_of_month"
                             f"\n\tspend_category"
                             f"\n\tbase_budget_amount"
                             f"\n\tperc_budget_amount"
                             f"\n\twaterfall_amount"
                             f"\n\tsaved_amount"
                             f"\n\tpercent_of_income_adjustment_amount")
        filepath = self.uns.request_open_filepath()
        data = pd.read_csv(filepath)
        if data is None:
            return

        ret = self._update_buckets_from_dataframe(account, data)
        if ret:
            self.uns.notify_user(f"Buckets data updated successfully from {filepath}")

    def _update_buckets_from_dataframe(self, account: Account, df: pd.DataFrame):
        try:
            logging.debug(df.dtypes)
            for index, row in df.iterrows():
                name = row['name']
                logging.debug(row)
                dsvca.update_bucket(account, name,
                                    priority=int(row["priority"]),
                                    due_day_of_month=int(row["due_day_of_month"]),
                                    spend_category=SpendCategory[row["spend_category"].upper()],
                                    base_budget_amount=float(row["base_budget_amount"]),
                                    perc_budget_amount=float(row["perc_budget_amount"]),
                                    waterfall_amount=float(row["waterfall_amount"]),
                                    saved_amount=float(row["saved_amount"]),
                                    percent_of_income_adjustment_amount=float(row["percent_of_income_adjustment_amount"]),
                                    provider=row["provider"] if pd.notna(row["provider"]) else "",
                                    payment_account=row["payment_account"] if pd.notna(row["payment_account"]) else "",
                                    payment_method=PaymentMethod[row["payment_method"].upper()] if pd.notna(row["payment_method"]) else ""
                                    )

            bucket_names_imported = set(x.upper() for x in df['name'])
            buckets = dsvca.buckets_by_account(account)
            for bucket in buckets:
                if bucket.name.upper() not in bucket_names_imported:
                    dsvca.delete_bucket_from_account(account, bucket.name)

            return True


        except Exception as e:
            error = f"Unable to import the dataset: {e}"
            self.uns.notify_user(error)
            self.uns.notify_user(df.columns)
            return False

    def positive_remaining_buckets(self, account: Account=None, amount_threshold: float = None):
        account = account if account else self.uns.select_account()

        buckets = dsvca.buckets_by_account(account)
        data = mongoHelper.list_mongo_to_pandas(buckets)
        filtered = data[data["saved_amount"] > 0].sort_values(by=["priority"])

        if amount_threshold is not None:
            filtered = filtered[filtered['saved_amount']>amount_threshold]

        return filtered

    def print_positive_remaining(self, account: Account=None, amount_threshold: float = None):
        filtered = self.positive_remaining_buckets(account, amount_threshold=amount_threshold)
        self.uns.pretty_print_items(filtered, title="Positive Remaining Buckets")

    def float_as_currency(self, val: float):
        return "${:,.2f}".format(round(val, 2))


    def plot_history_by_category(self):
        account = self.uns.select_account(statusList=[AccountStatus.ACTIVE.name])
        nMo = self.uns.request_int("Number of Relevant Months:")
        plt.plot_history_by_category(nMo, account=account, print_data=True)

    def plot_projected_finance(self):
        account = self.uns.select_account(statusList=[AccountStatus.ACTIVE.name])
        hist = self.uns.request_int("Relevant Historical Months:")
        future = self.uns.request_int("# Months to project:")
        current = self.uns.request_float("Current Balance:")

        plt.plot_projected_finance(hist, future, current, account=account)


if __name__ == "__main__":
    a = AccountManager()
    a.print_waterfall_summary()