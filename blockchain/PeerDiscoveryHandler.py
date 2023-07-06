import threading
import time
from Message import Message
from BlockchainUtils import BlockchainUtils
#Broadcast all the nodes, all peers in network
class PeerDiscoveryHandler():

    def __init__(self, node):
        self.socketCommunication = node

    def start(self):
        statusThread = threading.Thread(target=self.status,args=())
        statusThread.start()
        discoveryThread = threading.Thread(target=self.discovery,args=())
        discoveryThread.start()

    def status(self):
        while True:
            print('status')
            time.sleep(10)

    def discovery(self):
        while True:
            print('discovery')
            time.sleep(10)

    def handshake(self, connect_node): #exchange info between nodes
        handshakeMessage = self.handshakeMessage()
        self.socketCommunication.send(connect_node, handshakeMessage)
    
    def handshakeMessage(self):
        ownConnector = self.socketCommunication.socketConnector     
        ownPeers = self.socketCommunication.peers
        data = ownPeers
        messageType = 'DISCOVERY'
        message = Message(ownConnector, messageType, data)
        encodedMessage = BlockchainUtils.encode(message)
        return encodedMessage