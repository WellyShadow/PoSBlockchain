from flask_classful import FlaskView, route #logic behind
from flask import Flask, jsonify, request, render_template #app allows interact with endpoints
from BlockchainUtils import BlockchainUtils

node = None

class NodeAPI(FlaskView):

    def __init__(self):
        self.app = Flask(__name__)  #flask app

    def start(self, apiPort):
        NodeAPI.register(self.app, route_base='/')
        self.app.run(host = 'localhost', port = apiPort)

    def injectNode(self, injectednode):
        global node
        node = injectednode

    @route('/info', methods = ['GET'])
    def info(self):
        return render_template('index.html'), 200
    
    @route('/ok_mycryptowallet', methods = ['GET'])
    def ok_mycryptowallet(self):
        publicKeyString = node.wallet.publicKeyString()
        return render_template('ok_mycryptowallet.html',publicKeyString = publicKeyString), 200

    
    @route('/blockchain', methods = ['GET'])
    def blockchain(self):
        return node.blockchain.toJson(), 200
    
    @route('/transactionPool', methods = ['GET'])
    def transactionPool(self):
        transactions = {}
        for ctr, transaction in enumerate(node.transactionPool.transactions):#number of object and object itself
            transactions[ctr] = transaction.toJson()
        return jsonify(transactions), 200
    
    @route('/transaction', methods = ['POST'])
    def transaction(self):
        values = request.get_json()
        if not 'transaction' in values:
            return 'Missing transaction value', 400
        transaction = BlockchainUtils.decode(values['transaction'])
        node.handleTransaction(transaction)
        response = {'message':'Received transaction'}
        return jsonify(response), 200

    @route('/balance', methods = ['POST'])
    def balance(self):
        values = request.get_json()
        publicKeyString = values['publicKeyString']
        balance = node.blockchain.accountModel.getBalance(publicKeyString)
        return balance, 200
    
    @route('/address', methods = ['GET'])
    def address(self):
        publicKeyString = node.wallet.publicKeyString()
        return publicKeyString, 200
    
