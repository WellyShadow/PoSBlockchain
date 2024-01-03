from Ticket import Ticket
import copy

class Airplane():
    def __init__(self):
        self.fromWhere = "Київ"
        self.where = "Львів"
        self.date = "25.12.2023"
        self.timeDeparture = "9:00"
        self.timeArrival = "12:00"
        self.companyName = "МАУ"
        self.tickets = [Ticket() for _ in range(20)]

    def printTickets(self):
        for i in range (len(self.tickets)):
            print(i)
            print(self.tickets[i].price)
            print(self.tickets[i].ifbuy)
            print(self.tickets[i].id)

    def payload(self):
        jsonRepresentation = copy.deepcopy(self.toJson())
        jsonticket = []
        for ticket in self.tickets:
           jsonticket.append(ticket.toJson())
        jsonRepresentation['tickets'] = jsonticket
        jsonRepresentation['signature'] = ''
        return jsonRepresentation
    
    def toJson(self):
        return self.__dict__

    def addAirplane(self):
        self.tickets = [Ticket() for _ in range(20)]

