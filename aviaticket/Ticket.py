import uuid
class Ticket():
    def __init__(self):
        self.price = 10
        self.ifbuy = False
        self.id = uuid.uuid4()

    def toJson(self):
        return self.__dict__