from Transaction import Transaction
from Wallet import Wallet
from TransactionPool import TransactionPool
from Block import Block
from Blockchain import Blockchain
from BlockchainUtils import BlockchainUtils
import pprint
if __name__ == '__main__':

    sender = 'sender'
    receiver = 'receiver'
    amount = 1
    type = 'TRANSFER'

    wallet = Wallet()
    anotherwallet = Wallet()
    pool = TransactionPool()

    transaction = wallet.createTransaction(receiver,amount,type)
  
    if pool.transactionExists(transaction) == False:
        pool.addTransaction(transaction)
    
    blockchain = Blockchain()
    lastHash =  BlockchainUtils.hash(blockchain.blocks[-1].payload()).hexdigest()
    blockCount = blockchain.blocks[-1].blockCount + 1
    block = wallet.createBlock(pool.transactions, lastHash, blockCount)


    if not blockchain.lashBlockHashValid(block):
        print('LastBlockHash is not valid')
    if not blockchain.blockCountValid(block):
        print('BlockCount is not valid')

    if blockchain.lashBlockHashValid(block) and blockchain.blockCountValid(block):
        blockchain.addBlock(block)
    pprint.pprint(blockchain.toJson())
    



 