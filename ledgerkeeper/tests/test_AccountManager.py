import unittest

from ledgerkeeper.accountManager import AccountManager
from ledgerkeeper.mongoData.account import Account
from ledgerkeeper.tests.mock_AccountDataService import mock_AccountDataService
from ledgerkeeper.tests.mock_UserInteraction import mock_UserInteraction

class test_AccountManager(unittest.TestCase):


    def test_add_new_account(self):
        am = AccountManager()
        mockData = mock_AccountDataService()
        inputGet = mock_UserInteraction()
        account = am.add_new_account(accountDataService=mockData, inputGetter=inputGet)

        assert type(account) == Account

    def test_delete_account(self):
        am = AccountManager()
        mockData = mock_AccountDataService()
        inputGet = mock_UserInteraction()
        account = am.delete_account(accountDataService=mockData, inputGetter=inputGet)

        assert type(account) == Account







