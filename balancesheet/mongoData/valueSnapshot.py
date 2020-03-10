import mongoengine
import datetime

class ValueSnapshot(mongoengine.EmbeddedDocument):
    year = mongoengine.IntField(required=True)
    month = mongoengine.IntField(required=True)
    value = mongoengine.FloatField(required=True)
    recorded_date = mongoengine.DateTimeField(default=datetime.datetime.now)
