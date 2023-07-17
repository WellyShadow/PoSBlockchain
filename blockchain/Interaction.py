from Wallet import Wallet
from BlockchainUtils import BlockchainUtils
import requests


def postTransaction(sender, receiver, amount, type):
    transaction = sender.createTransaction(receiver.publicKeyString(), amount, type)

    url = 'http://localhost:5000/transaction'
    package = {'transaction': BlockchainUtils.encode(transaction)}
    request = requests.post(url, json = package)

if __name__ == '__main__':
    bob = Wallet()
    alise = Wallet()
    exchange = Wallet()
     
    alise.fromKey('keys/stakerPrivateKey.pem')


    postTransaction(exchange, alise, 100, 'EXCHANGE')
    postTransaction(exchange, bob, 100, 'EXCHANGE')
    postTransaction(exchange, bob, 10, 'EXCHANGE')

    postTransaction(alise, alise, 25, 'STAKE')
    postTransaction(alise, bob, 1, 'TRANSFER')
    postTransaction(alise, bob, 1, 'TRANSFER')
    postTransaction(alise, bob, 1, 'TRANSFER')