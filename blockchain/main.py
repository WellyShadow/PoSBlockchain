from Transaction import Transaction
from Wallet import Wallet
from TransactionPool import TransactionPool
from Block import Block
from Blockchain import Blockchain
from BlockchainUtils import BlockchainUtils
import pprint
from AccountModel import AccountModel
if __name__ == '__main__':

    wallet = Wallet()
    accountModel = AccountModel()

    accountModel.updateBalace(wallet.publicKeyString(), 10)
    accountModel.updateBalace(wallet.publicKeyString(), -5)

    print(accountModel.balances)
    



 