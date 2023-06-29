from Transaction import Trancastion
from Wallet import Wallet
if __name__ == '__main__':

    sender = 'sender'
    receiver = 'receiver'
    amount = 1
    type = 'TRANSFER'

    transaction = Trancastion(sender,receiver,amount,type)
    wallet = Wallet()
    signature = wallet.sign(transaction.toJson())

    transaction.sign(signature)

    signatureValid = Wallet.signatureValid(transaction.toJson(),signature, wallet.publicKeyString())
    print(transaction.toJson())
    print(signature)
    print(wallet.publicKeyString())
    print(signatureValid)
    