from Blockchain import Blockchain

class Node:
    def __init__(self, nodeID, nodeURL):
        self.NodeID  = nodeID
        self.SelfURL = nodeURL
        self.Chain = Blockchain()
