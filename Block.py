import time
from hashlib import sha256
import json


class Block:
    #For miner program will only take in blockHash input.
    def __init__(self, index=None, transactions=None, prevBlockHash=None, difficulty=None):
        self.dateCreated = time.time()
        self.difficulty = difficulty

        self.index=index
        self.transactions = transactions
        self.prevBlockHash = prevBlockHash

        self.nonce = 0
        self.minedBy = None;  # to be filled in by miner
        self.blockHash = None;  # to be filled in by miner

        if (index==0):
            blockData=""
            self.prevBlockHash = ""
        else:
            blockData = json.dumps([ob.__dict__ for ob in self.transactions])

        self.blockDataHash = sha256(blockData.encode()).hexdigest()
        self.blockString=   (str(self.dateCreated)+\
                                         str(self.difficulty)+\
                                         str(self.index)+ \
                                         self.prevBlockHash+\
                                         self.blockDataHash)

