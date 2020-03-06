import mongoengine

def global_init():

    data = dict()

    mongoengine.register_connection(alias='core', name='PersonalFinance', **data)