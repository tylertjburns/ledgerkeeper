import mongoengine

class Bucket(mongoengine.EmbeddedDocument):
    name = mongoengine.StringField(required=True)
    priority = mongoengine.IntField(default=99)
    due_day_of_month = mongoengine.IntField(default=99)
    spend_category = mongoengine.StringField(required=True)
    base_budget_amount = mongoengine.FloatField(default=0.0)
    perc_budget_amount = mongoengine.FloatField(default=0.0)
    waterfall_amount = mongoengine.FloatField(default=0.0)
    saved_amount = mongoengine.FloatField(default=0.0)
    percent_of_income_adjustment_amount = mongoengine.FloatField(default=0.0)

