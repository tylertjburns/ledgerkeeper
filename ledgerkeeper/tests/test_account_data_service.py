import unittest
from mongoengine import connect, disconnect
import ledgerkeeper.mongoData.account_data_service as ads
from ledgerkeeper.enums import AccountType

class test_account_data_service(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        connect('mongoenginetest', host='mongomock://localhost')

    @classmethod
    def tearDownClass(cls) -> None:
        disconnect()

    def test_enter_account(self):
        name = "test name"
        description = "test description"
        type = AccountType.PERSONAL
        ads.enter_account(name, description, type)

        account = ads.account_by_name(name)

        assert account.account_name == name
        assert account.description == description
        assert account.type == type.name
