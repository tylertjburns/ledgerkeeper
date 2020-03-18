import unittest
import mongoengine
from mongoengine.connection import _get_db

import ledgerkeeper.mongoData.account
from ledgerkeeper.accountManager import AccountManager
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
        self.db = mongoengine.disconnect()


    @patch('builtins.input', side_effect=['1', 'Test Name', 'Test Description'])
    def test_add_new_account(self, mock_input):
        userInteraction = FinanceCliInteraction()
        accountManager = AccountManager(userInteraction)
        account = accountManager.add_new_account()

        self.assertTrue(account.account_name == 'Test Name')
        self.assertTrue(account.type == AccountType.PERSONAL.name)




