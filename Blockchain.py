from Block import Block
import copy

class Blockchain:

    def __init__(self):
        self.blocks = []
        self.lastblock=None
        self.miningJob = None
        self.pendingTransactions=[]
        self.currentDifficulty = 3
        self.generateGenesisBlock()

    def addTransaction(self, transaction):
        self.pendingTransactions.append(transaction)

    def generateGenesisBlock(self):
        #def __init__(self, index, transactions, prevBlockHash, difficulty):
        genesisBlock = Block(0, None, None, None)
        self.blocks.append(genesisBlock)
        self.lastblock=genesisBlock

    def getMiningJob(self):
        #Let miner to get the blocktomine, only start next block when the current job/block mined
        if (self.miningJob==None):
            transactionsInBlock = copy.deepcopy(self.pendingTransactions)
            nextBlockindex = self.lastblock.index + 1
            prevBlockHash = self.lastblock.blockHash
            # (self, index, transactions, prevBlockHash):
            blockToMine = Block(nextBlockindex, transactionsInBlock, prevBlockHash, self.currentDifficulty)
            self.miningJob.append(blockToMine)
            self.pendingTransactions = []  # clear up pending transaction after txs are included in prevBlockHash the block.
        else:
            return self.miningJob;

