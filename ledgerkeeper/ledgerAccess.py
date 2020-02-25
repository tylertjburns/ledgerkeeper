import datetime
from uuid import uuid4
import logging
import data_service as dsvc
from runandcliscaffold.RunAndCliScaffold import RunAndCliScaffold
from enums import TransactionTypes

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
DATE_FORMAT = '%Y-%m-%d'


class LedgerManager(RunAndCliScaffold):
    def __init__(self):
        super().__init__("TESTING")

    def _defineFunctionsWithArgs(self):
        return {self.add_ledger: [{"short": "ds", "long": "date_stamp", "default": datetime.datetime.now(),
                                   "type": datetime.datetime, "help": "Ledger date of record"},
                                  {"short": "tid", "long": "transaction_id", "required": True,
                                   "type": str, "help": "Reference Transaction id of the ledger entry"},
                                  {"short": "dsc", "long": "description", "type": str, "required": True,
                                    "help": "short description of ledger item"},
                                  {"short": "tc", "long": "transaction_category", "type": str, "required": True,
                                    "help": "Category of the transaction for the ledger item"},
                                  {"short": "d", "long": "debit", "type": float, "default": 0,
                                   "help": "Debit (amount outgoing) of the ledger entry"},
                                  {"short": "c", "long": "credit", "type": float, "default": 0,
                                   "help": "Credit (amount incoming) of the ledger entry"},
                                  {"short": "fa", "long": "from_account", "type": str, "required": True,
                                   "help": "Which account is the ledger entry coming from"},
                                  {"short": "fb", "long": "from_bucket", "type": str, "required": True,
                                   "help": "Which bucket is the ledger entry coming from"},
                                  {"short": "ta", "long": "to_account", "type": str, "required": True,
                                   "help": "Which account is the ledger entry going to"},
                                  {"short": "tb", "long": "to_bucket", "type": str, "required": True,
                                   "help": "Which bucket is the ledger entry going to"},
                                  {"short": "n", "long": "notes", "type": str, "default": "",
                                   "help": "Additional notes regarding the ledger entry"},
                                  ],
        }

    def add_ledger(self, args):
        error = ""
        try:
            old_ledgers = dsvc.find_ledger_by_description_date_debit(args.description
                                                                    , args.date_stamp.date()
                                                                    , args.debit
                                                                    )
            if len(old_ledgers) > 0:
                raise Exception(
                    f"Ledger already exists for: "
                    f"\nDescription{args.description}"
                    f"\nDebit{args.debit}"
                    f"\nDate{args.date_stamp.date()}")

            dsvc.enter_ledger_entry(args.transaction_id
                                    , args.description
                                    , args.transaction_category
                                    , args.debit
                                    , args.credit
                                    , args.from_account
                                    , args.from_bucket
                                    , args.to_account
                                    , args.to_bucket
                                    , args.date_stamp
                                    , args.notes)
            ret = "Success"
        except ValueError as e:
            error = f"Incorrect date format. Expected format is {DATE_FORMAT} but {args.date_stamp} was provided"
            logging.error(error)
            ret = "Fail"
            raise ValueError(error)
        except Exception as e:
            error = f"Unable to add ledger entry: {e}"
            logging.error(error)
            ret = "Fail"
            raise Exception(error)
        finally:
            return {"return": ret, "error": error}

def _get_next_id():
    return str(uuid4())




def clear_ledger(**content):
    error = ""
    try:
        dsvc.clear_ledger()
        ret = "Success"
    except Exception as e:
        error = f"Unable to clear ledger: {e}"
        ret = "Fail"
        raise Exception(error)
    finally:
        return {"return": ret, "error": error}

def query_ledger(**query):
    error = ""
    try:
        ret = dsvc.query_ledger(query)
    except Exception as e:
        error = f"Unable to query {e}"
        logging.error(error)
        ret = "Fail"
        raise Exception(error)
    finally:
        return {"return": ret, "error": error}

if __name__ == "__main__":
    import loggingConfig
    import mongo_setup as ms
    ms.global_init()

    args = ['add_ledger'
        , "--transaction_id", '1'
        , "--transaction_category", TransactionTypes.APPLY_INCOME.name
        , "--description", f"MY DESCRIPTION - {_get_next_id()}"
        , "--credit", '100'
        , "--debit", '0'
        , "--from_account", "fAccount"
        , "--from_bucket", "fBucket"
        , "--to_account", "tAccount"
        , "--to_bucket", "tBucket"]

    exec = LedgerManager()
    exec.run()