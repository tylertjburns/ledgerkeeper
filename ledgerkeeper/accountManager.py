import mongoData.account_data_service as dsvca
from enums import SpendCategory, AccountType, CollectionType
from abstracts.userInteractionManager import UserIteractionManager

DEFAULT_BUCKET = "_DEFAULT"
CREDIT_BUCKET = "_CREDIT"
OTHER_BUCKET = "_OTHER"
TAX_WITHOLDING_BUCKET = "_TAXWITHOLDINGS"
PAY_WITH_REIMBURSEMENT_BUCKET = "_PAYWITHREIMBURSEMENT"


class AccountManager():
    def __init__(self, user_notification_system: UserIteractionManager):
        self.uns = user_notification_system


    def delete_account(self):
        name = self.uns.request_from_dict(dsvca.accounts_as_dict(), "Account Name:")

        if name is None:
            return

        account = dsvca.account_by_name(name)
        buckets = dsvca.buckets_by_account(account)
        
        waterfall_amt = 0
        saved_amt = 0
        for bucket in buckets:
            waterfall_amt += bucket.waterfall_amount
            saved_amt += bucket.saved_amount
        
        okay_to_delete = False
        if((waterfall_amt > 0) or (saved_amt > 0)):
            response = self.uns.request_from_dict({1: "Yes", 2: "No"})
            if response == "Yes":
                okay_to_delete = True
        else:
            okay_to_delete = True
        
        if okay_to_delete:
            dsvca.delete_account(name)
            self.uns.notify_user(f"Account {name} Deleted")
            
    def add_new_account(self):
        type = self.uns.request_enum(AccountType)
        name = self.uns.request_string("Account Name:")
        description = self.uns.request_string("Description:")

        account = dsvca.enter_if_not_exists(name=name, type=type, description=description)

        if account is not None:
            dsvca.add_bucket_to_account(account, DEFAULT_BUCKET, 99, 99, SpendCategory.OTHER.name)
            dsvca.add_bucket_to_account(account, CREDIT_BUCKET, 99, 99, SpendCategory.NA.name)
            dsvca.add_bucket_to_account(account, OTHER_BUCKET, 99, 99, SpendCategory.OTHER.name)
            dsvca.add_bucket_to_account(account, TAX_WITHOLDING_BUCKET, 99, 99, SpendCategory.OTHER.name)
            dsvca.add_bucket_to_account(account, PAY_WITH_REIMBURSEMENT_BUCKET, 99, 99, SpendCategory.NA.name)
            self.uns.notify_user("Account created successfully!")
        else:
            self.uns.notify_user(f"Error creating account. An account with the name {name} already exists.")

    def add_bucket_to_account(self):
        account = self.uns.request_from_dict(dsvca.accounts_as_dict(), prompt="Select an account:")
        name = self.uns.request_string("Bucket Name:")
        prio = self.uns.request_int("Priority:")
        due_day = self.uns.request_int("Due day of month:")
        category = self.uns.request_enum(SpendCategory)
        base_budget_amount = self.uns.request_float("Base budget amount:")

        bucket = dsvca.add_bucket_to_account(dsvca.account_by_name(account_name=account)
                                             , name=name
                                             , priority=prio
                                             , due_day_of_month=due_day
                                             , spend_category=category
                                             , base_budget_amount=base_budget_amount
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
        accountName = self.uns.request_from_dict(dsvca.accounts_as_dict(), "Select Account:")
        account = dsvca.account_by_name(accountName)
        fromB = self.uns.request_from_dict(dsvca.buckets_as_dict_by_account(account), "Select from bucket:")
        toB = self.uns.request_from_dict(dsvca.buckets_as_dict_by_account(account, set(fromB)), "Select to bucket:")
        amount = self.uns.request_float("Amount to move:", forcePos=True)

        fromBucket = dsvca.bucket_by_account_and_name(account, fromB)
        toBucket = dsvca.bucket_by_account_and_name(account, toB)

        dsvca.update_bucket_saved_amount(account, fromB, fromBucket.saved_amount - amount)
        dsvca.update_bucket_saved_amount(account, toB, toBucket.saved_amount + amount)

    def add_waterfall_funds(self):
        accountName = self.uns.request_from_dict(dsvca.accounts_as_dict(), "Account:")
        account = dsvca.account_by_name(accountName)
        amount = self.uns.request_float("Amount to add:", forcePos=True)
        buckets = dsvca.buckets_by_account(account)

        ''' Obtain a sortable list of keys that will be used for iterating through the waterfall'''
        iterSeq = sorted(list(bucket for bucket in buckets), key=lambda x: x.priority)

        ''' Iterate through the keys '''
        excess = amount
        keepExcess = False

        for bucket in iterSeq:
            adjustment = round(bucket.percent_of_income_adjustment_amount * amount, 2)
            dsvca.update_bucket_percentage_budget_amount(account, bucket.name, bucket.perc_budget_amount + adjustment)

            if (excess == 0):
                break

            if (bucket.name == DEFAULT_BUCKET):
                keepExcess = True

            excess = self._apply_waterfall_amount_to_bucket(account, bucket, excess, keepExcess=keepExcess)

        self.print_buckets(accountName=accountName)
        self.uns.notify_user(f"Amount: {amount} applied successfully")

    def _apply_waterfall_amount_to_bucket(self, account, bucket, amount, keepExcess=False):
        if (amount < 0):
            raise Exception(f"Error: Amount must be positive, {amount.amount} was entered.")

        dsvca.update_bucket_waterfall_amount(account, bucket.name, bucket.waterfall_amount + amount)

        waterfall_amount = bucket.waterfall_amount
        waterfall_amount += amount

        total_budget = bucket.base_budget_amount + bucket.perc_budget_amount
        if (bucket.waterfall_amount + amount > total_budget and not (keepExcess)):
            excess = bucket.waterfall_amount + amount - total_budget
            dsvca.update_bucket_waterfall_amount(account, bucket.name, total_budget)
        else:
            dsvca.update_bucket_waterfall_amount(account, bucket.name, bucket.waterfall_amount + amount)
            excess = 0.0

        self.uns.notify_user(f"{amount - excess} applied to bucket {bucket.name}", delay_sec=0)
        return excess

    def cycle_bucket(self, account, bucket):
        wf = bucket.waterfall_amount
        dsvca.update_bucket_saved_amount(account, bucket.name, bucket.saved_amount + wf)
        dsvca.update_bucket_waterfall_amount(account, bucket.name, 0)
        dsvca.update_bucket_percentage_budget_amount(account, bucket.name, 0)

    def delete_bucket_from_account(self):
        accountName = self.uns.request_from_dict(dsvca.accounts_as_dict(), prompt="Select an account:")
        bucketName = self.uns.request_string("Bucket Name:")

        account = dsvca.account_by_name(accountName)
        bucket = dsvca.delete_bucket_from_account(account, bucketName)

        self.uns.notify_user(f"Bucket {bucket.name} deleted from {account} successfully.")

