from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import PKCS1_v1_5
from BlockchainUtils import BlockchainUtils
from Transaction import Transaction
from Block import Block


class Wallet():

    node = None
    
    def __init__(self):
        self.keyPair = RSA.generate(2048)
        
            
    def __getstate__(self):
        return self.__dict__

    def __reduce__(self):
        return (self.__class__, ())

    def __setstate__(self, state):
        self.__dict__ = state
        

    def fromKey(self, file):
        key = ''
        with open(file, 'r') as keyfile:
            key = RSA.import_key(keyfile.read())
        self.keyPair = key
        
    def sign(self, data):
        dataHash = BlockchainUtils.hash(data)
        signatureSchemeObject = PKCS1_v1_5.new(self.keyPair)
        signature = signatureSchemeObject.sign(dataHash)
        return signature.hex()
         
    @staticmethod
    def signatureValid(data,signature,publicKeyString):
        signature = bytes.fromhex(signature)
        dataHash = BlockchainUtils.hash(data)
        publicKey = RSA.import_key(publicKeyString)
        signatureSchemeObject = PKCS1_v1_5.new(publicKey) 
        signatureValid = signatureSchemeObject.verify(dataHash,signature)
        return signatureValid

    def publicKeyString(self):
        publicKeyString = self.keyPair.publickey().exportKey('PEM').decode('utf-8')
        return publicKeyString
    
    def privateKeyString(self):
        privateKeyString = self.keyPair.exportKey('PEM').decode('utf-8')
        return privateKeyString
    
    def createTransaction(self,receiver,amount, type):
        transaction = Transaction(self.publicKeyString(),receiver,amount,type)
        signature = self.sign(transaction.payload())
        transaction.sign(signature)
        return transaction
    
    def createBlock(self, transaction, lashHash, blockCount):
        block = Block(transaction, lashHash, self.publicKeyString(), blockCount)
        signature = self.sign(block.payload())
        block.sign(signature)
        return block
