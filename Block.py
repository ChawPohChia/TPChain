import time
from hashlib import sha256
import json

# Index =""
# Transactions =""
# Difficulty=0
# PrevBlockHash={}
# MinedBy=""
# BlockDataHash=""
# Nonce=0
# DateCreated=""

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

        #blockData = json.dumps(self.transactions, default=obj_dict)  [ob.__dict__ for ob in list_name]
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



'''      
    def mine(self):
        blockHash=sha256((self.block_string+self.nonce).encode()).hexdigest()
        while not blockHash.startswith('0' * self.difficulty):
            self.nonce += 1
            blockHash = sha256((self.block_string + self.nonce).encode()).hexdigest()
        self.blockHash=blockHash;


'''