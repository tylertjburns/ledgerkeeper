import unittest
from mongoengine import connect, disconnect


class TestPerson(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        connect('mongoenginetest', host='mongomock://localhost', alias='test')

    @classmethod
    def tearDownClass(cls):
       disconnect()

    def test_thing(self):
        pers = Person(name='John')
        pers.save()

        fresh_pers = Person.objects().first()
        assert fresh_pers.name ==  'John'