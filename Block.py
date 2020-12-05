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
    def __init__(self, index, transactions, prevBlockHash, difficulty):
        self.dateCreated = time.time()
        self.difficulty = difficulty

        self.index=index
        self.transactions = transactions
        self.prevBlockHash = prevBlockHash

        #blockData = json.dumps(self.transactions, default=obj_dict)  [ob.__dict__ for ob in list_name]
        if (index==0):
            blockData=""
        else:
            blockData = json.dumps([ob.__dict__ for ob in self.transactions])

        self.blockDataHash = sha256(blockData.encode()).hexdigest()
        self.nonce = 0
        self.minedBy=None;
        self.blockHash = None;












    #BlockHash=""

