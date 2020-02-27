import mongoengine

class Account(mongoengine.Document):

    # Top Level Elements
    account_name = mongoengine.StringField(required=True)
    description = mongoengine.StringField(required=True)
    type = mongoengine.StringField(required=True)


    # Embedded Documents

    # Meta
    meta = {
        'db_alias': 'core',
        'collection': 'accounts'
    }