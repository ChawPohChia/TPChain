from Block import Block
import copy
from hashlib import sha256
from TPChainUtilities import getBlockHash, verifyBlockHash, strToDatetime

class Blockchain:

    def __init__(self):
        self.blocks = {}
        self.lastblock=None
        self.miningJob = None
        self.pendingTransactions=[]
        self.Difficulty = 3
        self.accounts={}
        self.generateGenesisBlock()


    def addTransaction(self, transaction):
        txVerified = self.verifyTransaction(transaction)
        if(txVerified):
            self.pendingTransactions.append(transaction)

    def verifyTransaction(self, transaction):
        print("verifying transactions...")
        return True;

    def generateGenesisBlock(self):
        self.blocks = {} #Clear all blocks while regenerate genesis block
        self.accounts = {} #Clear all accounts while regenerate genesis block
        #def __init__(self, index, transactions, prevBlockHash, difficulty):
        genesisBlock = Block(index=0, transactions="",prevBlockHash="",difficulty=self.Difficulty)
        #Self-mining of genesis block
        print("Genesis block mining is started...")
        blockHash = getBlockHash(genesisBlock.blockString, genesisBlock.nonce)

        #self mining here for genesis block
        while not blockHash.startswith('0' * self.Difficulty):
            genesisBlock.nonce += 1
            blockHash = getBlockHash(genesisBlock.blockString, genesisBlock.nonce)

        genesisBlock.blockHash = blockHash;
        print("Nonce found for genesis block: " + str(genesisBlock.nonce))
        print("Blockhash: " + genesisBlock.blockHash)
        self.blocks.update({0:genesisBlock})
        self.lastblock=genesisBlock

    def getSingleAddressOldestTransactionOnly(self, pendingTransactions):
        uniqueTransactions = []
        for ptx in pendingTransactions:
            toSkip = False;
            for element in pendingTransactions:
                if ((ptx.data["from"] == element.data["from"]) & (strToDatetime(ptx.data["dateCreated"]) > strToDatetime(element.data["dateCreated"]))):
                    toSkip = True;
            if (not toSkip):
                uniqueTransactions.append(ptx)

        for tx in uniqueTransactions:
            pendingTransactions.remove(tx)

        return uniqueTransactions

    def createMiningJob(self):
        # Let miner to get the blocktomine, only start next block when the current job/block mined
        if ((self.miningJob == None) & (len(self.pendingTransactions)!=0)):
            transactionsInBlock = self.getSingleAddressOldestTransactionOnly(self.pendingTransactions) ## Very important! While copy job as preparation for txs,
                                                                                                       ##      only one unique to-address in each txs in block
            nextBlockindex = self.lastblock.index + 1
            prevBlockHash = self.lastblock.blockHash
            blockToMine = Block(nextBlockindex, transactionsInBlock, prevBlockHash, self.Difficulty)
            self.miningJob = blockToMine

    def getMiningJob(self):
        #Let miner to get the blocktomine, only start next block when the current job/block mined
        self.createMiningJob()
        if(self.miningJob!=None):
            miningJobIndict={"Index":self.miningJob.index,"Blockstring": self.miningJob.blockString, "Difficulty":self.miningJob.difficulty}
        else:
            miningJobIndict = {}
        return miningJobIndict

    def verifyAndSubmitBlock(self, index, nonce, miner):
        if ((index in self.blocks)|(index!=self.miningJob.index)): # Block has been mined
            return False,"Apologise, block has been mined or mining job not exist!"

        verified, blockHash, vrfMessage = verifyBlockHash(self.miningJob.blockString,nonce, self.Difficulty)
        if(verified):
            self.miningJob.nonce=nonce
            self.miningJob.minedBy = miner
            self.miningJob.blockHash = blockHash
            self.blocks.update({index: self.miningJob}) # Persist block to blocks
            self.lastblock = self.miningJob  # Update last block
            self.miningJob = None  # Clear up the job after persist to blocks
            ## Need to update the transactions status also - WIP...\
            
            #need to update status of the transaction here
            
            self.createMiningJob() #Create mining job immediately after mining done.
            
            return True, "Congrats! Your mined block has been accepted!" #WIP: Need to pay mining fee for miner here/








