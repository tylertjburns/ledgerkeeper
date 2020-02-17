from pymongo import MongoClient
from enum import Enum
import click
import datetime

class TransactionTypes(Enum):
    APPLY_PAYMENT = 1
    APPLY_INCOME = 2
    MOVE_FUNDS = 3
    BALANCE_BANK = 4


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
DATE_FORMAT = '%Y-%m-%d'

def mongo_connect(mongodb_url):
    return MongoClient(mongodb_url)

def personal_finance_db(mongodb_url):
    return mongo_connect(mongodb_url)["PersonalFinance"]

def ledger_collection(mongodb_url, testmode):
    if testmode is None or testmode is False:
        return personal_finance_db(mongodb_url)["ledger"]
    else:
        return personal_finance_db(mongodb_url)["test_ledger"]

def add_ledger_to_mongo(**content):
    error = ""
    try:
        date_obj = datetime.datetime.strptime(content.get('date_stamp', str(datetime.date.today()), DATE_FORMAT),
                                              DATE_FORMAT)

        document = {
            'date_stamp': date_obj,
            'transaction_id': content['transaction_id'],
            'description': content['description'],
            'transaction_category': content['transaction_category'],
            'debit': content['debit'],
            'credit': content['credit'],
            'from_account': content['from_account'],
            'from_bucket': content['from_bucket'],
            'to_account': content['to_account'],
            'to_bucket': content['to_bucket'],
            'amount_covered': 0,
            'refunded': 0,
            'notes': content.get('notes', "")
        }


        collection = ledger_collection(content['mongo_db_url'], content.get('testmode', None))
        collection.insert_one(document)
        ret = "Success"
    except ValueError as e:
        error = f"Incorrect date format. Expected format is {DATE_FORMAT} but {content.get('date_stamp')} was provided"
        ret = "Fail"
        raise ValueError(error)
    except Exception as e:
        error = f"Unable to add ledger entry: {e}"
        ret = "Fail"
        raise Exception(error)
    finally:
        print(f"{ret} {error}")
        return {"return": ret, "error": error}

@click.group(context_settings=CONTEXT_SETTINGS)
def run():
    pass


@run.command()
@click.argument('mongo_db_url', type=str)
@click.argument('transaction_id', type=str)
@click.argument('transaction_category', type=click.Choice([str(x.name) for x in TransactionTypes]))
@click.argument('description', type=str)
@click.argument('credit', type=float)
@click.argument('debit', type=float)
@click.argument('from_account', type=str)
@click.argument('from_bucket', type=str)
@click.argument('to_account', type=str)
@click.argument('to_bucket', type=str)
@click.option('--date_stamp', type=click.DateTime(formats=[DATE_FORMAT]), default=str(datetime.date.today()), help='specify a date for the transaction if it is not today')
@click.option('--notes', default='', type=str, help="used to add detailed comments to the ledger entry")
def add(**kwargs):
    return add_ledger_to_mongo(**kwargs)

@run.command()
def get(**kwargs):
    collection = ledger_collection()

    results = collection.find()

    for result in results:
        print(result)

if __name__ == "__main__":
    run()