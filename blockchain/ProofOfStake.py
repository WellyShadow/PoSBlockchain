


class ProofOfStake():
    
    def __init__(self):
        self.stackers = {}
    
    def update(self, publicKeyString, stake):
        if publicKeyString in self.stackers.keys():
            self.stackers[publicKeyString] += stake
        else:
            self.stackers[publicKeyString] = stake

    def get(self, publicKeyString):
        if publicKeyString in self.stackers.keys():
            return self.stackers[publicKeyString]
        else:
            return None