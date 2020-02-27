import mongoengine
import datetime

class Transaction(mongoengine.Document):

    # Top Level Elements
    date_stamp = mongoengine.DateTimeField(default=datetime.datetime.now, format='%m/%d/%Y %H:%M:%S')

    transaction_id = mongoengine.StringField(required=True, primary_key=True)
    source = mongoengine.StringField(required=True)
    category = mongoengine.StringField(required=True)
    description = mongoengine.StringField(required=True)
    debit = mongoengine.FloatField(required=True)
    credit = mongoengine.FloatField(required=True)

    handled = mongoengine.StringField(required=True)
    # Embedded Documents

    # Meta
    meta = {
        'db_alias': 'core',
        'collection': 'transactions'
    }