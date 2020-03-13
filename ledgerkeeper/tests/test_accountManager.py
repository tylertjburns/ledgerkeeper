import unittest
import mongoengine
from mongoengine.connection import _get_db

import ledgerkeeper.mongoData.account
from ledgerkeeper.accountManager import AccountManager
from userInteraction.financeCliInteraction import FinanceCliInteraction

from ledgerkeeper.enums import AccountType

from unittest.mock import patch





class test_AccountManager(unittest.TestCase):
    # def __init__(self):
    #     super().__init__(self)
    #     self.db = None

    # @classmethod
    # def setUpClass(cls):
    #     mongoengine.connect('mongoenginetest', host='mongomock://localhost')
    #
    # @classmethod
    # def tearDownClass(cls):
    #    mongoengine.disconnect()

    @classmethod
    def setUpClass(self) -> None:
        mongoengine.connect('mongoenginetest',  host='localhost:27017', alias='core')

    @classmethod
    def tearDownClass(self) -> None:
        mongoengine.disconnect()


    @patch('builtins.input', side_effect=['1', 'Test Name', 'Test Description'])
    def test_add_new_account(self, mock_input):
        userInteraction = FinanceCliInteraction()
        accountManager = AccountManager(userInteraction)
        account = accountManager.add_new_account()

        self.assertTrue(account.account_name == 'Test Name')
        self.assertTrue(account.type == AccountType.PERSONAL.name)




