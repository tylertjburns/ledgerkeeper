import mongoengine
import datetime

class Transaction(mongoengine.Document):

    # Top Level Elements
    date_stamp = mongoengine.DateTimeField(default=datetime.datetime.now, format='%m/%d/%Y %H:%M:%S')

    id = mongoengine.StringField(required=True)
    source = mongoengine.StringField(required=True)
    category = mongoengine.StringField(required=True)
    description = mongoengine.StringField(required=True)
    debit = mongoengine.FloatField(required=True)
    credit = mongoengine.FloatField(required=True)
    # Embedded Documents

    # Meta
    meta = {
        'db_alias': 'core',
        'collection': 'transactions'
    }