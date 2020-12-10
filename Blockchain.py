from Block import Block
import copy
from hashlib import sha256

class Blockchain:

    def __init__(self):
        self.blocks = []
        self.lastblock=None
        self.miningJob = None
        self.pendingTransactions=[]
        self.Difficulty = 3
        self.generateGenesisBlock()

    def addTransaction(self, transaction):
        self.pendingTransactions.append(transaction)

    def generateGenesisBlock(self):
        #def __init__(self, index, transactions, prevBlockHash, difficulty):
        genesisBlock = Block(index=0, transactions="",prevBlockHash="",difficulty=self.Difficulty)
        #Self-mining of genesis block
        print("Genesis block mining is started...")
        blockHash = sha256((genesisBlock.blockString + str(genesisBlock.nonce)).encode()).hexdigest()
        #blockHash = sha256((genesisBlock.blockString + genesisBlock.nonce)).hexdigest()
        while not blockHash.startswith('0' * self.Difficulty):
            genesisBlock.nonce += 1
            blockHash = sha256((genesisBlock.blockString + str(genesisBlock.nonce)).encode()).hexdigest()
            #blockHash = sha256((genesisBlock.blockString + genesisBlock.nonce)).hexdigest()
        genesisBlock.blockHash = blockHash;
        print("Nonce found for genesis block: " + str(genesisBlock.nonce))
        print("Blockhash: " + genesisBlock.blockHash)

        self.blocks.append(genesisBlock)
        self.lastblock=genesisBlock

    def getMiningJob(self):
        #Let miner to get the blocktomine, only start next block when the current job/block mined
        if (self.miningJob==None):
            transactionsInBlock = copy.deepcopy(self.pendingTransactions)
            nextBlockindex = self.lastblock.index + 1
            prevBlockHash = self.lastblock.blockHash
            # (self, index, transactions, prevBlockHash):
            blockToMine = Block(nextBlockindex, transactionsInBlock, prevBlockHash, self.Difficulty)
            self.miningJob = blockToMine
            self.pendingTransactions = []  # clear up pending transaction after txs are included in prevBlockHash the block.

        miningJobIndict={"Index":self.miningJob.index,"Blockstring": self.miningJob.blockString, "Difficulty":self.miningJob.difficulty}
        return miningJobIndict;

