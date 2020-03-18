
from ledgerkeeper.enums import HandleTransactionMethod, TransactionTypes, TransactionStatus, \
    TransactionSplitType, SpendCategory, AccountStatus, PaymentType, TransactionSource
from enums import CollectionType
import ledgerkeeper.mongoData.transaction_data_service as dsvct
import ledgerkeeper.mongoData.ledger_data_service as dsvcl
from userInteraction.interfaces.IFinanceInteraction import IFinanceInteraction
import uuid

import plotter as plt

class LedgerManager():
    def __init__(self, user_notification_system: IFinanceInteraction):
        self.uns = user_notification_system

    def add_ledger_manually(self):
        input = self.uns.get_add_ledger_manually_input()
        trans_id = str(uuid.uuid4())

        # Add transaction for reference
        transaction = dsvct.enter_if_not_exists(transaction_category=input['transaction_category']
                                                , transaction_id=trans_id
                                                , description=input['description']
                                                , debit=input['debit']
                                                , credit=input['credit']
                                                , source=TransactionSource.MANUALENTRY
                                                , date_stamp=input['date_stamp']
                                                , payment_type=input['payment_type']
                                                , handled=TransactionStatus.HANDLED)

        ledger = dsvcl.enter_if_not_exists(transaction_id=trans_id
                                           , description=input['description']
                                           , transaction_category=input['transaction_category']
                                           , debit=input['debit']
                                           , credit=input['credit']
                                           , from_account=input['from_account'].account_name
                                           , from_bucket=input['from_bucket'].name
                                           , to_account=input['to_account'].account_name
                                           , to_bucket=input['to_bucket'].name
                                           , source=TransactionSource.MANUALENTRY
                                           , spend_category=input['spend_category']
                                           , payment_type=input['payment_type']
                                           , date_stamp=input['date_stamp']
                                           , notes=input['notes'])

        if ledger is None:
            self.uns.notify_user("Ledger item already exists")
            return

        self.uns.notify_user("Ledger Entry added successfully")

    def query_ledger(self):
        query = self.uns.request_string("Query:")
        dsvcl.query_ledger(query)

    def print_ledger(self):
        account = self.uns.select_account(statusList=[AccountStatus.ACTIVE.name])
        items_json = dsvcl.query_ledger("", account_names=[account.account_name]).to_json()
        self.uns.pretty_print_items(items_json, title=CollectionType.LEDGER.name)

    def delete_a_ledger_item(self):
        id = self.uns.request_string("ID:")

        success = dsvcl.delete_by_id(id)
        if success == 1:
            self.uns.notify_user(f"Ledger item {id} deleted")
        else:
            self.uns.notify_user(f"Ledger with id {id} not found")

