from Block import Block
import copy
from hashlib import sha256
from TPChainUtilities import getBlockHash, verifyBlockHash, strToDatetime

class Blockchain:

    def __init__(self):
        self.Difficulty = 3
        self.TotalTPCoin = 1000000
        self.TPFoundationWalletAddress="1AzKmHdg6j8jPA8sNpxc2z7BMsKLCXRp6L"
        self.FaucetAddress = "1EmQd4rXvNEoWLKRNSdnb2GP9i5VQwuaEM"

        self.blocks = {}
        self.lastblock=None
        self.miningJob = None

        self.rejectedTransactions = []  # Transaction with blockindex=-3
        self.pendingTransactions=[]     #Transaction with blockindex=-2
        self.inProcessTransactions = []  #Transaction with blockindex=-1
        self.completedTransactions = [] #Transaction with blockindex>0

        self.balances={}
        self.generateGenesisBlock()
        self.runInitialCoinDistribution()

    def runInitialCoinDistribution(self):
        coinForTPFoundation = 500000 #(50%)
        coinForFaucet = 100000 #(10%)

        #WIP: The followings Should implement transaction mechanism
        self.TotalTPCoin -= coinForFaucet
        self.balances["1EmQd4rXvNEoWLKRNSdnb2GP9i5VQwuaEM"]=coinForFaucet
        self.TotalTPCoin -= coinForTPFoundation
        self.balances["1AzKmHdg6j8jPA8sNpxc2z7BMsKLCXRp6L"]=coinForTPFoundation


    def addTransaction(self, transaction):
        txVerified = self.verifyTransaction(transaction)
        if(txVerified):
            print("Transaction is added in PendingTransaction collection.")
            self.pendingTransactions.append(transaction)
        else:
            print("Transaction is added in rejectedTransaction collection.")
            self.rejectedTransactions.append(transaction)

    def verifyTransaction(self, transaction):
        #data: {"from": "1Asq3p1PdSW39sRWSceiPDP5uTmrYawESW", "to": "XxnoCyJMtY323Y7mG6ePWtAmCoTH7KGqxX",
        #       "value": 100000,
        #       "fee": 100, "dateCreated": "2020-12-1 16:4:38"}
        if (transaction.data["from"] not in self.balances.keys()):
            transaction.setBlockIndexRemarks(-3,"Account is not found!")
            return False;
        if(self.balances[transaction.data["from"]]<int(transaction.data["value"])):
            transaction.setBlockIndexRemarks(-3,"Insufficient fund")
            return False;
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

    def getSingleAddressOldestTransactionOnlyIntoInProcessList(self):
        uniqueTransactions = []
        for ptx in self.pendingTransactions:
            toSkip = False;
            for element in self.pendingTransactions:
                if ((ptx.data["from"] == element.data["from"]) & (strToDatetime(ptx.data["dateCreated"]) > strToDatetime(element.data["dateCreated"]))):
                    toSkip = True;
            if (not toSkip):
                uniqueTransactions.append(ptx)

        for tx in uniqueTransactions:
            tx.setBlockIndexRemarks(-1,"")
            self.inProcessTransactions.append(tx)
            self.pendingTransactions.remove(tx)

        return uniqueTransactions

    def createMiningJob(self):
        # Let miner to get the blocktomine, only start next block when the current job/block mined
        if ((self.miningJob == None) & (len(self.pendingTransactions)!=0)):
            self.getSingleAddressOldestTransactionOnlyIntoInProcessList() ## Very important! While copy job as preparation for txs,
                                                                                                                  ##      only one unique to-address in each txs in block
            nextBlockindex = self.lastblock.index + 1
            prevBlockHash = self.lastblock.blockHash
            blockToMine = Block(nextBlockindex, self.inProcessTransactions, prevBlockHash, self.Difficulty)
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

            # Update transaction index/status
            for tx in self.miningJob.transactions:
                tx.setBlockIndexRemarks(self.miningJob.index,"Mined in Block "+ str(self.miningJob.index))
                self.inProcessTransactions.remove(tx)
                self.completedTransactions.append(tx)

            

            self.miningJob = None  # Clear up the job after persist to blocks
            self.createMiningJob() #Create mining job immediately after mining done.
            
            return True, "Congrats! Your mined block has been accepted!" #WIP: Need to pay mining fee for miner here/








