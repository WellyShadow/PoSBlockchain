from flask_classful import FlaskView, route #logic behind
from flask import Flask, jsonify, request, render_template, redirect, url_for #app allows interact with endpoints
from BlockchainUtils import BlockchainUtils
import urllib.parse
from Wallet import Wallet
import requests

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
    
    @route('', methods = ['GET'])
    def info(self):
        global company 
        company = Wallet()
        return render_template('index.html'), 200
    
    @route('/ok_mycryptowallet')
    def ok_mycryptowallet(self, publicKeyString=0):
        outputResult = 0
        balance = 0
        publicKeyString = request.args.get('publicKeyString')
        if publicKeyString is not None:
            lines = publicKeyString.split('\\n')
            for i in range(2, len(lines)-2):
                lines[i] = lines[i].replace(' ', '+')
            result = '\n'.join(lines)
            balance = node.blockchain.accountModel.getBalance(result)

            begin_marker = "-----BEGIN PUBLIC KEY-----"
            end_marker = "-----END PUBLIC KEY-----"
            start_index = result.find(begin_marker) + len(begin_marker)
            end_index = result.find(end_marker)
            public_key_data = result[start_index:end_index]
            first_four_chars = public_key_data[:5]
            last_four_chars = public_key_data[-5:]
            outputResult = first_four_chars + "-" + last_four_chars
        return render_template('ok_mycryptowallet.html',publicKeyString = outputResult,balance = balance), 200

    
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
    
    @route('/tickets', methods = ['GET'])
    def tickets(self):
        tickets = node.blockchain.airplane.payload()
        return tickets, 200
    
    

    @route('/price', methods = ['GET'])
    def price(self):
        price = node.blockchain.airplane.tickets[0].id
        return str(price), 200
    
    @route('/balanceTicket', methods = ['POST'])
    def balanceTicket(self):
        values = request.get_json()
        publicKeyString = values['publicKeyString']
        print(publicKeyString)
        print(type(publicKeyString))
        balance = node.blockchain.accountModel.getBalance(publicKeyString)
        return str(balance), 200
    
    @route('/signin', methods = ['GET'])
    def signin(self):
        return render_template('sign_in.html')
    
    @route('/reg', methods = ['GET'])
    def reg(self):
        return render_template('create_wallet.html')
    
    @route('/createwallet')
    def createwallet(self):
        wallet = Wallet()
        publicKeyString = wallet.publicKeyString()
        return redirect (url_for('NodeAPI:ok_mycryptowallet',publicKeyString = publicKeyString))
    
    @route('/tx')
    def tx(self):
        publicKeyString = request.args.get('publicKeyString')
        transaction = company.createTransaction(publicKeyString, 40, 'EXCHANGE')
        url = 'http://localhost:5000/transaction'
        package = {'transaction': BlockchainUtils.encode(transaction)}
        response = requests.post(url, json = package)
        return render_template('reservation_places.html')

    
    @route('/reservationplaces')
    def reservationplaces(self):
        publicKeyString = request.args.get('publicKeyString')
        if publicKeyString is not None:
            lines = publicKeyString.split('\\n')
            for i in range(2, len(lines)-2):
                lines[i] = lines[i].replace(' ', '+')
            publicKeyString = '\n'.join(lines)
            return redirect (url_for('NodeAPI:tx', publicKeyString = publicKeyString))
        return render_template('reservation_places.html')
    
    