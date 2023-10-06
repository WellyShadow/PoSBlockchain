from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import PKCS1_v1_5
from BlockchainUtils import BlockchainUtils
from Transaction import Transaction
from Block import Block
from AccountModel import AccountModel

class Wallet():

    node = None
    
    def __init__(self):
        self.keyPair = RSA.generate(2048)
        
        #nodeWallet = NodeWalletCommunication()
            
    def __getstate__(self):
        return self.__dict__

    def __reduce__(self):
        return (self.__class__, ())

    def __setstate__(self, state):
        self.__dict__ = state
        #Wallet.node_instance = None
        #self.node_instance = None
        #self.node = None
        #self.accModel = AccountModel.get_a()
        #self.blockchain = blockchain
        
    #def setAccountModel(self, account_model):
    #    self.accModel = account_model
    #@classmethod
    #def setNode(cls, node):
    #        if cls.node is None:
    #            cls.node = node
    #            print('in setNode',type(cls.node))

    #@classmethod
    #def getNode(cls):
    #    print('in getNode cls',type(cls.node))
    #    return cls.node

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

    #def injectblockchain(self, injectedblockchain):
    #    global blockchain
     #   blockchain = injectedblockchain
    #def balance(self):
        #self.getAccModel()
        #publicKeyString = self.publicKeyString()
        #print(publicKeyString)
        #blockchain = Node.getBlockchain()
        #self.injectblockchain(blockchain)
        #node = Wallet.getNode()
        #print(1)
        #if Wallet.node_instance is not None:
        #blockchain = Wallet.node_instance.blockchain
        #balance = blockchain.accountModel.balances
        #print(balance)
        #return balance
        #else:
        #print("Node не был установлен в классе Wallet")

        #print(balance)
        #return balance