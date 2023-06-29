from transaction import Trancastion

if __name__ == '__main__':

    sender = 'sender'
    receiver = 'receiver'
    amount = 1
    type = 'TRANSFER'

    transaction = Trancastion(sender,receiver,amount,type)
    print(transaction.toJson())