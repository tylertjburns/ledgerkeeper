from click.testing import CliRunner
import unittest
import sys, os
root_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..\\..'))
sys.path.append(root_path)
import ledgerkeeper.ledgerAccess as la


class test_ledgerAccess(unittest.TestCase):
    def test_add_ledger_to_mongo(self):
        result = la.add_ledger_to_mongo(**{
        "mongo_db_url": "mongodb://localhost/PersonalFinance?"
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

        print(result["error"])
        assert result["return"] == "Success"
        assert result["error"] == ""

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