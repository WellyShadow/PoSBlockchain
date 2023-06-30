import time
import copy
class Block():
   
    def __init__(self, transactions, lastHash, forger, blockCount):
      self.transactions = transactions
      self.lastHash = lastHash
      self.forger = forger
      self.blockCount = blockCount
      self.timestamp = time.time()
      self.signature = ''

    def toJson(self):
        data = {}
        data['lashHash'] = self.lastHash
        data['forget'] = self.forger
        data['blockCount'] = self.blockCount
        data['timestamp'] = self.timestamp
        data['signature'] = self.signature
        jsonTransaction = []
        for transaction in self.transactions:
           jsonTransaction.append(transaction.toJson())
        data['transactions'] = jsonTransaction
        return data
    
    def payload(self):
        jsonRepresentation = copy.deepcopy(self.toJson())
        jsonRepresentation['signature'] = ''
        return jsonRepresentation
    
    def sign (self, signature):
       self.signature = signature
           