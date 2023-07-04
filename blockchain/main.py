from Transaction import Transaction
from Wallet import Wallet
from TransactionPool import TransactionPool
from Block import Block
from Blockchain import Blockchain
from BlockchainUtils import BlockchainUtils
import pprint
from AccountModel import AccountModel
if __name__ == '__main__':

    blockchain = Blockchain()
    pool = TransactionPool()

    alice = Wallet()
    bob = Wallet()

    #alise wants to send 5 tokens to bob

    transaction = alice.createTransaction(bob.publicKeyString(), 5, 'TRANSFER')

    if not pool.transactionExists(transaction):
        pool.addTransaction(transaction)

    coveredTransaction = blockchain.getCoveredTransactionSet(pool.transactions)

    print(coveredTransaction)
    



 