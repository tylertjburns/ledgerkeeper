import mongoengine
from ledgerkeeper.mongoData.bucket import Bucket
from ledgerkeeper.enums import AccountStatus

class Account(mongoengine.Document):

    # Top Level Elements
    account_name = mongoengine.StringField(required=True)
    description = mongoengine.StringField(required=True)
    type = mongoengine.StringField(required=True)
    status = mongoengine.StringField(default=AccountStatus.ACTIVE.name)

    # Embedded Documents
    buckets = mongoengine.EmbeddedDocumentListField(Bucket)

    # Meta
    meta = {
        'db_alias': 'core',
        'collection': 'accounts'
    }

