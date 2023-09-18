from Wallet import Wallet
from BlockchainUtils import BlockchainUtils
import requests


def postTransaction(sender, receiver, amount, type):
    transaction = sender.createTransaction(receiver.publicKeyString(), amount, type)

    url = 'http://localhost:5000/transaction'
    package = {'transaction': BlockchainUtils.encode(transaction)}
    request = requests.post(url, json = package)

#def getBalance(bob):
#    response = requests.post('http://localhost:5000/balance', json={'publicKeyString': bob.publicKeyString()})
#    balance = response.text
#    print(f"Balance for Bob: {balance}")

if __name__ == '__main__':
    bob = Wallet()
    exchange = Wallet()
    company = Wallet()
    #node = Wallet.getNode()
    #print(type(node))
    #alise.fromKey('keys/stakerPrivateKey.pem')
    #node = NodeAPI.returnNode()
    #print('after', type(node))
    #response = requests.post('http://localhost:5000/balance', json={'publicKeyString': bob.publicKeyString()})
    #balance = response.text
    #print(f"Balance for Bob: {balance}")
    #postTransaction(exchange, alise, 100, 'EXCHANGE')
    #getBalance(bob)
    postTransaction(exchange, bob, 100, 'EXCHANGE')
    postTransaction(exchange, bob, 10, 'EXCHANGE')
    postTransaction(exchange, bob, 50, 'EXCHANGE')
    postTransaction(exchange, bob, 40, 'EXCHANGE')
    postTransaction(bob, company, 10, 'BUYTICKET')
    postTransaction(exchange, bob, 10, 'EXCHANGE')
    postTransaction(exchange, bob, 20, 'EXCHANGE')
    #response = requests.post('http://localhost:5000/balance', json={'publicKeyString': bob.publicKeyString()})
    #balance = response.text
    #print(f"Balance for Bob: {balance}")
    #postTransaction(alise, alise, 25, 'STAKE')
    #postTransaction(alise, bob, 1, 'TRANSFER')
    #postTransaction(alise, bob, 1, 'TRANSFER')
    #postTransaction(alise, bob, 1, 'TRANSFER')