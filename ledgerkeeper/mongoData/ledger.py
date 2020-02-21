import mongoengine
import datetime

class LedgerItem(mongoengine.Document):

    # Top Level Elements
    date_stamp = mongoengine.DateTimeField(default=datetime.datetime.now, format='%m/%d/%Y %H:%M:%S')

    transaction_id = mongoengine.StringField(required=True)
    description = mongoengine.StringField(required=True)
    transaction_category = mongoengine.StringField(required=True)
    debit = mongoengine.FloatField(required=True)
    credit = mongoengine.FloatField(required=True)
    from_account = mongoengine.StringField(required=True)
    from_bucket = mongoengine.StringField(required=True)
    to_account = mongoengine.StringField(required=True)
    to_bucket = mongoengine.StringField(required=True)

    amount_covered = mongoengine.FloatField(default=0)
    refunded = mongoengine.FloatField(default=0)
    notes = mongoengine.StringField(default="")

    # Embedded Documents

    # Meta
    meta = {
        'db_alias': 'core',
        'collection': 'ledger'
    }