from click.testing import CliRunner
import unittest
import sys, os
root_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..\\..'))
sys.path.append(root_path)
import ledgerkeeper.ledgerAccess as la


TEST_MONGO_URL = "mongodb://localhost/PersonalFinance?"

class test_ledgerAccess(unittest.TestCase):
    def test_add_ledger_to_mongo(self):
        result = la.add_ledger_to_mongo(**{
        "mongo_db_url": TEST_MONGO_URL
        , "transaction_id": 1
        , "transaction_category": la.TransactionTypes.APPLY_INCOME.name
        , "description": "MY DESCRIPTION"
        , "credit": 100
        , "debit": 0
        , "from_account": "fAccount"
        , "from_bucket": "fBucket"
        , "to_account": "tAccount"
        , "to_bucket": "tBucket"
        , "testmode": True
        })

        assert result["return"] == "Success"
        assert result["error"] == ""

    def test_clear_ledger(self):
        result = la.clear_ledger(**{
            "mongo_db_url": TEST_MONGO_URL
            , "testmode": True
        })

        assert result["return"] == "Success"

    def test_query_ledger(self):
        clear = la.clear_ledger(**{
            "mongo_db_url": TEST_MONGO_URL
            , "testmode": True
        })

        for ii in range(0, 5):
            add = la.add_ledger_to_mongo(**{
            "mongo_db_url": TEST_MONGO_URL
            , "transaction_id": ii
            , "transaction_category": la.TransactionTypes.APPLY_INCOME.name
            , "description": "MY DESCRIPTION"
            , "credit": 100
            , "debit": 0
            , "from_account": "fAccount"
            , "from_bucket": "fBucket"
            , "to_account": "tAccount"
            , "to_bucket": "tBucket"
            , "testmode": True
            })


        result = la.query_ledger()

        assert len(result["return"]) == 4
        assert len(result["return"]) != "Fail"


    # def test_add(self):
    #     runner = CliRunner()
    #     result = runner.invoke(la.add, [
    #         "mongodb://localhost/PersonalFinance?"
    #         , 1
    #         , la.TransactionTypes.APPLY_INCOME.name
    #         , "MY DESCRIPTION"
    #         , 100
    #         , 0
    #         , "fAccount"
    #         , "fBucket"
    #         , "tAccount"
    #         , "tBucket"
    #     ])
    #     assert result.exit_code == 0