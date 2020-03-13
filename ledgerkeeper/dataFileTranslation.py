import pandas as pd
from ledgerkeeper.enums import TransactionTypes, TransactionSource, TransactionStatus, SpendCategory, PaymentType
import ledgerkeeper.mongoData.transaction_data_service as dsvct
import ledgerkeeper.mongoData.ledger_data_service as dsvcl
import uuid
from dateutil import parser
from ledgerkeeper.mongoData.account import Account

def _float_from_dollar_string(input):
    ret = input.replace('$', '').replace(' ', '').replace(',', '')

    if ret == "" or ret is None:
        return 0
    else:
        return float(ret)

def read_in_pnc_transactions(filepath: str):
    # Read in the PNC data from csv
    pnc_data = pd.read_csv(filepath).fillna(0.0)

    #Translate PNC transactions to standard transaction format
    pnc_transactions = []
    for transaction in pnc_data.to_dict('rows'):
        if type(transaction['Credit']) != float:
            credit = _float_from_dollar_string(transaction["Credit"])
        else:
            credit = transaction["Credit"]

        if type(transaction['Debit']) != float:
            debit = _float_from_dollar_string(transaction["Debit"])
        else:
            debit = transaction["Debit"]

        if credit > 0:
            transaction_category = TransactionTypes.APPLY_INCOME
        else:
            transaction_category = TransactionTypes.RECORD_EXPENSE



        new = dsvct.enter_if_not_exists(transaction_category=transaction_category
                                        , transaction_id=str(uuid.uuid4())
                                        , description=transaction['Transaction']
                                        , debit=debit
                                        , credit=credit
                                        , payment_type=PaymentType.BANK
                                        , source=TransactionSource.PNC
                                        , date_stamp=parser.parse(transaction['Date']))

        if new is not None:
            pnc_transactions.append(new)

    return pnc_transactions

def read_in_barclay_transactions(filepath: str):
    # Read in the BarclayCardUs data from csv
    barclay_data = pd.read_csv(filepath, skiprows=[0, 1, 2, 3], )

    # Transalate BarclayCardUs transactions to standard transaction format
    barclay_transactions = []
    for transaction in barclay_data.to_dict('rows'):
        if transaction['Category'] == 'DEBIT':
            debit = -transaction["Amount"]
            credit = 0
            transaction_category = TransactionTypes.RECORD_EXPENSE
        elif transaction['Category'] == 'CREDIT' and transaction['Description'] == 'PaymentReceived':
            debit = 0
            credit = transaction['Amount']
            transaction_category = TransactionTypes.APPLY_PAYMENT
        elif transaction['Category'] == 'CREDIT' and transaction['Description'] != 'PaymentReceived':
            debit = 0
            credit = transaction['Amount']
            transaction_category = TransactionTypes.RECEIVE_REFUND
        else:
            raise Exception(f"Unhandled transaction category for BarclaycardUS: {transaction['Category']}")

        new = dsvct.enter_if_not_exists(transaction_category=transaction_category
                                        , transaction_id=str(uuid.uuid4())
                                        , description=transaction['Description']
                                        , debit=debit
                                        , credit=credit
                                        , source=TransactionSource.BARCLAYCARDUS
                                        , payment_type=PaymentType.CREDIT
                                        , date_stamp=parser.parse(transaction['Transaction Date']))

        if new is not None:
            barclay_transactions.append(new)

    return barclay_transactions

def read_in_old_ledgers(filepath: str, account: Account):
    # Read in the old ledger data from csv
    old_data = pd.read_csv(filepath, encoding='ISO-8859-1').fillna("")



    # Transalate old ledger data into standard ledger format
    old_ledgers = []
    for ledger in old_data.to_dict('rows'):
        if ledger['Trans_Type'] == 'APPLY PMNT':
            debit = _float_from_dollar_string(ledger['Amount'])
            credit = 0.0
            transaction_category = TransactionTypes.RECORD_EXPENSE
        elif ledger['Trans_Type'] == 'MOVING FUNDS':
            debit = _float_from_dollar_string(ledger['Amount'])
            credit = _float_from_dollar_string(ledger['Amount'])
            transaction_category = TransactionTypes.MOVE_FUNDS
        elif ledger['Trans_Type'] == 'ADD INCOME':
            debit = 0.0
            credit = _float_from_dollar_string(ledger['Amount'])
            transaction_category = TransactionTypes.APPLY_INCOME
        elif ledger['Trans_Type'] == 'BALANCE BANK':
            debit = 0.0
            credit = _float_from_dollar_string(ledger['Amount'])
            transaction_category = TransactionTypes.BALANCE_BANK
        elif ledger['Trans_Type'] == "CHANGE MONTH":
            continue
        else:
            raise Exception(f"Unhandled transaction category for Archive: {ledger['Trans_Type']}")

        from_bucket = ledger['From']
        to_account = ledger['To']

        if ledger['Spend_Cat'] == 'Car' and ledger['From'] == "Car (AUTO_PNC)":
            spend_category = SpendCategory.CARPAYMENT
        elif ledger['Spend_Cat'] == 'Car':
            spend_category = SpendCategory.CARMAINT
        else:
            spend_category = old_spend_category_switch(ledger['Spend_Cat'])

        trans_id = str(uuid.uuid4())

        if ledger['Trans_Type'] == 'APPLY PMNT' and ledger['To'] == "PAYMENT - Credit":
            payment_type = PaymentType.CREDIT
        elif ledger['Trans_Type'] == 'APPLY PMNT' and ledger['To'] == "PAYMENT - Bank-PNC":
            payment_type = PaymentType.BANK
        elif ledger['Trans_Type'] == 'APPLY PMNT' and ledger['To'] == "PAYMENT - Cash":
            payment_type = PaymentType.CASH
        else:
            payment_type = PaymentType.NOTAPPLICABLE

        # Add transaction fro reference
        transaction = dsvct.enter_if_not_exists(transaction_category=transaction_category
                                                , transaction_id=trans_id
                                                , description=ledger['Comment']
                                                , debit=debit
                                                , credit=credit
                                                , source=TransactionSource.ARCHIVE
                                                , date_stamp=parser.parse(ledger['Date'])
                                                , payment_type=payment_type
                                                , handled=TransactionStatus.HANDLED)


        # Unsure about format, but confident no duplicates, therefore dont check for dups before entering
        new = dsvcl.enter_ledger_entry(
                                    transaction_id=trans_id
                                    , transaction_category=transaction_category
                                    , description=ledger['Comment']
                                    , debit=debit
                                    , credit=credit
                                    , source=TransactionSource.ARCHIVE
                                    , from_account=account.account_name
                                    , from_bucket=from_bucket
                                    , to_bucket=to_account
                                    , to_account=to_account
                                    , spend_category=spend_category
                                    , payment_type=payment_type
                                    , date_stamp=parser.parse(ledger['Date'])
                                    , notes=ledger['Comment'])


        if new is not None:
            old_ledgers.append(new)

    return old_ledgers

def old_spend_category_switch(old:str):
    try:
        return SpendCategory[old.upper()]
    except:
        switcher = {
            "": SpendCategory.NOTAPPLICABLE,
            "Income": SpendCategory.NOTAPPLICABLE,
            "Investment": SpendCategory.INVESTMENT,
            "_NA": SpendCategory.NOEXPENSE,
            "Fun": SpendCategory.FUN,
            "Gas": SpendCategory.FUEL,
            "Giving": SpendCategory.CHARITY,
            "Groceries": SpendCategory.GROCERIES,
            "Home Living": SpendCategory.GENERALHOMEEXPENSE,
            "Insurance": SpendCategory.CARINSURANCE,
            "Loan": SpendCategory.LOANPAYMENT,
            "Medical": SpendCategory.MEDICAL,
            "Other": SpendCategory.OTHER,
            "Phone": SpendCategory.PHONE,
            "Rent / Mortgage": SpendCategory.RENT_MORTGAGE,
            "Rent/Mortgage": SpendCategory.RENT_MORTGAGE,
            "Spending Allowance": SpendCategory.SPENDINGALLOWANCE,
            "Travel": SpendCategory.TRAVEL,
            "Utilities": SpendCategory.UTILITIES,
            "Vacation": SpendCategory.VACATION,
            "Wallace": SpendCategory.PETS,
            "Work Meals": SpendCategory.GENERALLIVINGEXPENSE,
            "Work Supplies": SpendCategory.OTHER
        }
        return switcher[old]