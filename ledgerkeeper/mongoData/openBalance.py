import mongoengine

class OpenBalance(mongoengine.EmbeddedDocument):
    name = mongoengine.StringField(required=True)
    entry_date = mongoengine.DateTimeField(required=True)
    amount = mongoengine.FloatField(required=True)

