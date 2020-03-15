import unittest
import mongoengine

from ledgerkeeper.accountManager import AccountManager
from ledgerkeeper.ledgerManager import LedgerManager
from userInteraction.financeCliInteraction import FinanceCliInteraction

from ledgerkeeper.enums import AccountType

from unittest.mock import patch



class test_AccountManager(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(test_AccountManager, self).__init__(*args, **kwargs)
        self.db = None

    @classmethod
    def setUpClass(self) -> None:
        self.db = mongoengine.connect('mongoenginetest',  host='localhost:27017', alias='core')

    @classmethod
    def tearDownClass(self) -> None:
        mongoengine.disconnect()
        self.db.drop_database('mongoenginetest')


    @patch('builtins.input', side_effect=['1', 'Test Name', 'Test Description'])
    def test_add_new_account(self, mock_input):
        userInteraction = FinanceCliInteraction()
        accountManager = AccountManager(userInteraction)
        account = accountManager.add_new_account()

        self.assertTrue(account.account_name == 'Test Name')
        self.assertTrue(account.type == AccountType.PERSONAL.name)

    @patch('builtins.input', side_effect=['1', '1'])
    def test_delete_account(self, mock_input):
        userInteraction = FinanceCliInteraction()
        accountManager = AccountManager(userInteraction)
        ledgerManager = LedgerManager(userInteraction)
        success = accountManager.delete_account(ledgerManager)

        self.assertTrue(success)








