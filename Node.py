class Node:
    NodeID =""
    SelfURL=""
    peers={}
    Chain={}

    def __init__(self, nodeID, nodeURL):
        self.NodeID  = nodeID
        self.SelfURL = nodeURL
