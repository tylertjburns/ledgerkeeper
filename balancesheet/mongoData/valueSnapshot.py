import mongoengine

class ValueSnapshot(mongoengine.EmbeddedDocument):
    year = mongoengine.StringField(required=True)
    month = mongoengine.IntField(required=True)
    value = mongoengine.FloatField(required=True)
