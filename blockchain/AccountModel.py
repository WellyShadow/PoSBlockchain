class AccountModel():

    def __init__(self):
        self.accounts = []
        self.balances = {}
        self.tickets = {}
    
    def addAccount(self, publicKeyString):
        if not publicKeyString in self.accounts:
            self.accounts.append(publicKeyString)
            self.balances[publicKeyString] = 0
            self.tickets[publicKeyString] = []
    
    def getBalance(self,publicKeyString):
        if publicKeyString not in self.accounts:
            self.addAccount(publicKeyString)
        return self.balances[publicKeyString]
    
    def updateBalace(self,publicKeyString, amount):
        if publicKeyString not in self.accounts:
            self.addAccount(publicKeyString)
        self.balances[publicKeyString] += amount

    def getBalanceTicket(self,publicKeyString):
        if publicKeyString not in self.accounts:
            self.addAccount(publicKeyString)
        return self.tickets[publicKeyString]

    def updateTicket(self,publicKeyString, ticket):
        if publicKeyString not in self.accounts:
            self.addAccount(publicKeyString)
        self.tickets[publicKeyString].append(ticket)
