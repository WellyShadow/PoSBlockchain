from flask_classful import FlaskView, route #logic behind
from flask import Flask #app allows interact with endpoints


class NodeAPI(FlaskView):

    def __init__(self):
        self.app = Flask(__name__)  #flask app

    def start(self):
        NodeAPI.register(self.app, route_base='/')
        self.app.run(host = 'localhost')

    @route('/info', methods = ['GET'])
    def info(self):
        return 'This is communication interface to a nodes blockcahin', 200
