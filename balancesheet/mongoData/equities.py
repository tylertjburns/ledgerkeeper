import mongoengine
from balancesheet.mongoData.valueSnapshot import ValueSnapshot

class Equity(mongoengine.Document):

    # Top Level Elements
    name = mongoengine.StringField(required=True)
    description = mongoengine.StringField(required=True)
    account_id = mongoengine.StringField(required=True)
    equityClass = mongoengine.StringField(required=True)
    equityType = mongoengine.StringField(required=True)
    interestRate = mongoengine.FloatField(default=0.0)
    equityTimeHorizon = mongoengine.StringField(required=True)
    equityStatus = mongoengine.StringField(required=True)
    equityContingency = mongoengine.StringField(required=True)

    # Embedded Documents
    snapshots = mongoengine.EmbeddedDocumentListField(ValueSnapshot)

    # Meta
    meta = {
        'db_alias': 'core',
        'collection': 'equities'
    }

