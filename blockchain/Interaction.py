from Wallet import Wallet
from BlockchainUtils import BlockchainUtils
import requests

if __name__ == '__main__':
    bob = Wallet()
    alise = Wallet()
    exchange = Wallet()

    transaction = exchange.createTransaction(alise.publicKeyString(), 10, 'EXCHANGE')

    url = 'http://localhost:5000/transaction'
    package = {'transaction': BlockchainUtils.encode(transaction)}
    request = requests.post(url, json = package)
    print(request.text)