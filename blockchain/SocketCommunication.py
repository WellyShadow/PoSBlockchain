from p2pnetwork.node import Node


class SocketCommunication (Node):

    def __init__(self, ip, port):
        super(SocketCommunication, self).__init__(ip, port, None)

    def startSocketCommunication(self):
        self.start()

    def inbound_node_connected(self, connected_node):
        print('inbound connection')
        self.send_to_node(connected_node,'Hi i am node you connected to')
    
    def outbound_node_connected(self, connected_node):
        print('outbound connection')
        self.send_to_node(connected_node,'Hi i am the node who initialized the connection')

    def node_message(self, connected_node, message):
        print(message)

