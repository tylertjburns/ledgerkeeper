import mongoengine

def global_init():
    # data = dict()

    # mongoengine.register_connection(alias='core', name='PersonalFinance', **data)


    mongoengine.connect('PersonalFinance', host='localhost:27017', alias='core')
