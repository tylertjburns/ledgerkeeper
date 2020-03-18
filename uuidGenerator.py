from interfaces.IIdGenerator import IIdGenerator
import uuid

class UuidGenerator(IIdGenerator):
    def generate_new_id(self):
        return uuid.uuid4()
