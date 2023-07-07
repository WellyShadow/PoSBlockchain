from flask_classful import FlaskView, route #logic behind
from flask import Flask #app allows interact with endpoints

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
        return 'This is communication interface to a nodes blockcahin', 200
    
    @route('/blockchain', methods = ['GET'])
    def blockchain(self):
        return node.blockchain.toJson(), 200
