import pandas as pd
import os
import sys
import decimal
from enums import TransactionTypes, TransactionSource, TransactionStatus
import mongoData.transaction_data_service as dsvct
import uuid
from dateutil import parser

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



        new = dsvct.enter_if_not_exists(transaction_category=transaction_category.name
                                      , transaction_id=str(uuid.uuid4())
                                      , description=transaction['Transaction']
                                      , debit=debit
                                      , credit=credit
                                      , source=TransactionSource.PNC.name
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

        new = dsvct.enter_if_not_exists(transaction_category=transaction_category.name
                                      , transaction_id=str(uuid.uuid4())
                                      , description=transaction['Description']
                                      , debit=debit
                                      , credit=credit
                                      , source=TransactionSource.BARCLAYCARDUS.name
                                      , date_stamp=parser.parse(transaction['Transaction Date']))

        if new is not None:
            barclay_transactions.append(new)

        # barclay_transactions.append(create_standard_transaction(**{
        #     "datestamp": transaction['Transaction Date'],
        #     "source": "BarclayCardUs",
        #     "debit": debit,
        #     "credit": credit,
        #     "description": transaction['Description'],
        #     "category": transaction_category
        # }))

    return barclay_transactions



