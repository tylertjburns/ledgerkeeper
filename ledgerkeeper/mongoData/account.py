import mongoengine
from mongoData.bucket import Bucket

class Account(mongoengine.Document):

    # Top Level Elements
    account_name = mongoengine.StringField(required=True)
    description = mongoengine.StringField(required=True)
    type = mongoengine.StringField(required=True)


    # Embedded Documents
    buckets = mongoengine.EmbeddedDocumentListField(Bucket)

    # Meta
    meta = {
        'db_alias': 'core',
        'collection': 'accounts'
    }

