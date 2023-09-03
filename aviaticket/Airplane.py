from Ticket import Ticket

class Airplane():
    def __init__(self):
        self.fromWhere = "Лондон"
        self.where = "Париж"
        self.date = "05.09.2023"
        self.timeDeparture = "16:40"
        self.timeArrival = "20:40"
        self.companyName = "American Airline"
        self.tickets = []

    def printTickets(self):
        for i in range (10):

            print(self.tickets[i].price)
            print(self.tickets[i].ifbuy)
            print(self.tickets[i].id)

    def addAirplane(self):
        self.tickets = [Ticket() for _ in range(20)]

