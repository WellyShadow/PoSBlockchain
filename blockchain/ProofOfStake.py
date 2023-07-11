from Lot import Lot
from BlockchainUtils import BlockchainUtils

class ProofOfStake():
    
    def __init__(self):
        self.stackers = {}
        self.setGenesisNodeStake()

    def setGenesisNodeStake(self):
        genesisPublicKey = open('keys/genesisPublicKey.pem', 'r').read()
        self.stackers[genesisPublicKey] = 1
    
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
        
    def validatorLots(self, seed):
        lots = []
        for validator in self.stackers.keys():
            for stake in range(self.get(validator)):
                lots.append(Lot(validator, stake + 1, seed))
        return lots
    
    def winnerLot(self, lots, seed):
        winnerLot = None
        leastOffset = None
        referenceHashIntValue = int(BlockchainUtils.hash(seed).hexdigest(), 16)
        for lot in lots:
            lotIntValue = int(lot.lotHash(), 16)
            offset = abs(lotIntValue - referenceHashIntValue)
            if leastOffset is None or offset < leastOffset:
                leastOffset = offset
                winnerLot = lot
        return winnerLot
    
    def forger(self, lastBlockHash):
        lots = self.validatorLots(lastBlockHash)
        winnerLot = self.winnerLot(lots, lastBlockHash)
        return winnerLot.publicKey