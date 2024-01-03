from flask_classful import FlaskView, route #logic behind
from flask import Flask, jsonify, request, render_template, redirect, url_for, session #app allows interact with endpoints
from BlockchainUtils import BlockchainUtils
import urllib.parse
from Wallet import Wallet
import requests
import pickle
node = None

class NodeAPI(FlaskView):

    def __init__(self):
        self.app = Flask(__name__)  #flask app
        self.app.secret_key = 'supersecretkey1'

    def start(self, apiPort):
        NodeAPI.register(self.app, route_base='/')
        self.app.run(host = 'localhost', port = apiPort)

    def injectNode(self, injectednode):
        global node
        node = injectednode
    

    @route('/clickon_ok_mycryptowallet')
    def clickon_ok_mycryptowallet(self):
        publicKeyString = session.get('publicKeyString')
        return redirect (url_for('NodeAPI:ok_mycryptowallet',publicKeyString = publicKeyString))

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
        return render_template('ok_mycryptowallet.html',publicKeyStringShort = outputResult,
                               publicKeyString=result,balance = balance), 200

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
    
    @route('index', methods = ['GET'])
    def index(self,publicKeyString=0):
        publicKeyString = session.get('publicKeyString')
        if publicKeyString is None:
            return render_template('index.html')  
        return redirect (url_for('NodeAPI:index_inacc', publicKeyString = publicKeyString))

    @route('', methods = ['GET'])
    def startPage(self,publicKeyString=0):
        global company 
        company = Wallet()
        publicKeyString = session.get('publicKeyString')
        if publicKeyString is None:
            return render_template('index.html')  
        return redirect (url_for('NodeAPI:index_inacc', publicKeyString = publicKeyString))
    
    @route('/index_inacc', methods = ['GET'])
    def index_inacc(self,publicKeyString=0):
        publicKeyString = request.args.get('publicKeyString')
        return render_template ('index_inacc.html')
    
    @route('/clickonreservation', methods = ['GET'])
    def clickonreservation(self):
        publicKeyString = session.get('publicKeyString')
        return redirect (url_for('NodeAPI:reservation', publicKeyString = publicKeyString))

    @route('/reservation', methods = ['GET'])
    def reservation(self, publicKeyString = 0):
        return render_template('reservation.html',publicKeyString=publicKeyString)
    
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
        privateKeyString = wallet.privateKeyString()
        print(publicKeyString)
        session['publicKeyString'] = publicKeyString
        session['wallet'] = pickle.dumps(wallet)
        return redirect (url_for('NodeAPI:aftercreatewallet',publicKeyString = publicKeyString, privateKeyString = privateKeyString))
    
    @route('/aftercreatewallet', methods = ['GET'])
    def aftercreatewallet(self,publicKeyString = 0, privateKeyString = 0):
        publicKeyString = request.args.get('publicKeyString')
        privateKeyString = request.args.get('privateKeyString')
        if publicKeyString is not None:
            lines = publicKeyString.split('\\n')
            for i in range(2, len(lines)-2):
                lines[i] = lines[i].replace(' ', '+')
            result = '\n'.join(lines)
            print(result)
        return render_template('aftercreatewallet.html',publicKeyString = result, privateKeyString = privateKeyString)
    
    @route('/continue_aftersave', methods = ['GET'])
    def continue_aftersave(self ):
        publicKeyString = session.get('publicKeyString')
        if publicKeyString is not None:
            lines = publicKeyString.split('\\n')
            for i in range(2, len(lines)-2):
                lines[i] = lines[i].replace(' ', '+')
            result = '\n'.join(lines)
        return redirect (url_for('NodeAPI:ok_mycryptowallet',publicKeyString = result))
    
    
    @route('/topup_balance')
    def topup_balance(self):
        publicKeyString = session.get('publicKeyString')
        
        transaction = company.createTransaction(publicKeyString, 3000, 'EXCHANGE')
        url = 'http://localhost:5000/transaction'
        package = {'transaction': BlockchainUtils.encode(transaction)}
        response = requests.post(url, json = package)
        return redirect (url_for('NodeAPI:ok_mycryptowallet',publicKeyString = publicKeyString))
    
    
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
    
    @route('/choosed_ticket')
    def choosed_ticket(self, publicKeyString=0):
        publicKeyString = session.get('publicKeyString')
        if publicKeyString is not None:
            lines = publicKeyString.split('\\n')
            for i in range(2, len(lines)-2):
                lines[i] = lines[i].replace(' ', '+')
            publicKeyString = '\n'.join(lines)
            return redirect (url_for('NodeAPI:order_tickets', publicKeyString = publicKeyString))
        return render_template('order_tickets.html')
        
    @route('/order_tickets')
    def order_tickets(self, publicKeyString = 0):
        return render_template('order_tickets.html', publicKeyString = publicKeyString)

    @route('/continue_order_tickets')
    def continue_order_tickets(self, publicKeyString=0):
        publicKeyString = session.get('publicKeyString')
        if publicKeyString is not None:
            lines = publicKeyString.split('\\n')
            for i in range(2, len(lines)-2):
                lines[i] = lines[i].replace(' ', '+')
            publicKeyString = '\n'.join(lines)
            return redirect (url_for('NodeAPI:reservation_aboutpass', publicKeyString = publicKeyString))
        return render_template('reservation_aboutpass.html')
    
    @route('/reservation_aboutpass')
    def reservation_aboutpass(self, publicKeyString = 0):
        return render_template('reservation_aboutpass.html', publicKeyString = publicKeyString)
    


    @route('/continue_reservation_aboutpass')
    def continue_reservation_aboutpass(self, publicKeyString=0):
        publicKeyString = session.get('publicKeyString')
        if publicKeyString is not None:
            lines = publicKeyString.split('\\n')
            for i in range(2, len(lines)-2):
                lines[i] = lines[i].replace(' ', '+')
            publicKeyString = '\n'.join(lines)
            return redirect (url_for('NodeAPI:reservation_places', publicKeyString = publicKeyString))
        return render_template('reservation_places.html')
    
    @route('/reservation_places')
    def reservation_places(self, publicKeyString = 0):
        return render_template('reservation_places.html', publicKeyString = publicKeyString)
    
    @route('/payment_reservation_places')
    def payment_reservation_places(self, publicKeyString=0):
        publicKeyString = session.get('publicKeyString')
        if publicKeyString is not None:
            lines = publicKeyString.split('\\n')
            for i in range(2, len(lines)-2):
                lines[i] = lines[i].replace(' ', '+')
            publicKeyString = '\n'.join(lines)
            return redirect (url_for('NodeAPI:overview', publicKeyString = publicKeyString))
        return render_template('overview.html')
    
    @route('/overview')
    def overview(self, publicKeyString = 0):
        return render_template('overview.html', publicKeyString = publicKeyString)
    
    @route('/buy_ticket')
    def buy_ticket(self):
        publicKeyString = request.args.get('publicKeyString')
        wallet = pickle.loads(session.get('wallet'))
        transaction = wallet.createTransaction(company.publicKeyString(), 10, 'BUYTICKET')
        url = 'http://localhost:5000/transaction'
        package = {'transaction': BlockchainUtils.encode(transaction)}
        response = requests.post(url, json = package)
        return redirect (url_for('NodeAPI:complete_tx', publicKeyString = publicKeyString))
    
    @route('/pay_overview')
    def pay_overview(self, publicKeyString=0):
        publicKeyString = session.get('publicKeyString')
        if publicKeyString is not None:
            lines = publicKeyString.split('\\n')
            for i in range(2, len(lines)-2):
                lines[i] = lines[i].replace(' ', '+')
            publicKeyString = '\n'.join(lines)
            return redirect (url_for('NodeAPI:buy_ticket', publicKeyString = publicKeyString))
        return render_template('complete_tx.html')
    
    @route('/complete_tx')
    def complete_tx(self, publicKeyString = 0):
        return render_template('complete_tx.html', publicKeyString = publicKeyString)