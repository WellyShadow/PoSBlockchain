import threading
import time

#Broadcast all the nodes, all peers in network
class PeerDiscoveryHandler():

    def __init__(self, node):
        self.socketCommunication = node

    def start(self):
        statusThread = threading.Thread(self.status,args=())
        statusThread.start()
        discoveryThread = threading.Thread(self.discovery,args=())
        discoveryThread.start()

    def status(self):
        while True:
            print('status')
            time.sleep(10)

    def discovery(self):
        while True:
            print('discovery')
            time.sleep(10)

    
        