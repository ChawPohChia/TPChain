from Block import Block
import copy
from hashlib import sha256
from TPChainUtilities import getBlockHash, verifyBlockHash, strToDatetime
from datetime import datetime as dt

class Blockchain:

    def __init__(self):
        self.Difficulty = 3
        self.TotalTPCoin = 1000000
        self.NetworkCoinBalance =  self.TotalTPCoin
        self.TPFoundationWalletAddress="1AzKmHdg6j8jPA8sNpxc2z7BMsKLCXRp6L"
        self.FaucetAddress = "1EmQd4rXvNEoWLKRNSdnb2GP9i5VQwuaEM"
        self.FaucetRequestAmount=10

        self.faucetRequestRecords = {}
            #"abcabc": ["2021-01-31 16:14:39", "2021-02-01 23:4:39", "2021-02-03 16:4:37", "2021-02-04 03:14:38",
            #           "2021-3-31 16:14:39"], "cdecde": ["2020-12-4 16:4:38", "2020-12-5 16:4:38"]}

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
        self.NetworkCoinBalance  -= coinForFaucet
        self.balances["1EmQd4rXvNEoWLKRNSdnb2GP9i5VQwuaEM"]=coinForFaucet
        self.NetworkCoinBalance  -= coinForTPFoundation
        self.balances["1AzKmHdg6j8jPA8sNpxc2z7BMsKLCXRp6L"]=coinForTPFoundation

        ## For testing purpose
        #self.balances["XxnoCyJMtY323Y7mG6ePWtAmCoTH7KGqxX"] = coinForTPFoundation
    
    def checkAccountBalance(self, address):
        if address not in self.balances.keys():
            return (-1,"Account not in the network")
        else: 
            return (self.balances[address],"Retrieve Account balance successfully")

    def checkAccountTransactions(self, address):
        if address not in self.balances.keys():
            return (-1,"Account not in the network")
        else:
            relevantTransactions = self.checkCollectionsForTransaction(address)
            if (len(relevantTransactions)==0):
                return(0,"There is no relevant transactions found.")
            else:
                return (len(relevantTransactions),relevantTransactions)
        
    def checkCollectionsForTransaction(self, address):
        collectionsToCheck=[self.rejectedTransactions,self.completedTransactions,self.inProcessTransactions, self.pendingTransactions]
        addressTransactions=[]
        for collection in collectionsToCheck:
            for tx in collection:
                if (tx.data["from"]==address or tx.data["to"]==address):
                    addressTransactions.append(tx);
        return addressTransactions;
            
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
            transaction.setBlockIndexRemarks(-3,"Sender account is not found!")
            return False;

        if (transaction.data["to"] not in self.balances.keys()):
            transaction.setBlockIndexRemarks(-3, "Recipient account is not found!")
            return False;

        if(self.balances[transaction.data["from"]]<int(transaction.data["value"])):
            transaction.setBlockIndexRemarks(-3,"Insufficient fund")
            return False;
        return True;

    def checkFaucetRequestGreediness(self,addressSendTo,currentRequestDatetime):
        if addressSendTo not in self.faucetRequestRecords.keys():
            return False; #No request history found so is not greedy

        for record in self.faucetRequestRecords[addressSendTo]:
            historyRecord = dt.strptime(record, "%Y-%m-%d %H:%M:%S")
            currentRequest = dt.strptime(currentRequestDatetime, "%Y-%m-%d %H:%M:%S")
            if((currentRequest - historyRecord).days <1): #Return true if any history found with creation within 1 day
                return True;
        return False;

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
            miningJobTransactions=self.getSingleAddressOldestTransactionOnlyIntoInProcessList() ## Very important! While copy job as preparation for txs,
                                                                                                                  ##      only one unique to-address in each txs in block
            nextBlockindex = self.lastblock.index + 1
            prevBlockHash = self.lastblock.blockHash
            blockToMine = Block(nextBlockindex, miningJobTransactions, prevBlockHash, self.Difficulty)
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

            # Update transaction index/status
            for tx in self.miningJob.transactions:
                tx.setBlockIndexRemarks(self.miningJob.index,"Mined in Block "+ str(self.miningJob.index)) ##??? ties to inProcessTransactionAlready

                self.balances[tx.data["from"]] -= int(tx.data["value"])
                self.balances[tx.data["to"]] += int(tx.data["value"])

                ##Record Faucet success request for greeding checking
                if(tx.data["from"] == self.FaucetAddress):
                    if (tx.data["to"] not in self.faucetRequestRecords):
                        self.faucetRequestRecords[tx.data["to"]] = [tx.data["dateCreated"]] #create a new collection as one of the dictionary element
                else:
                    self.faucetRequestRecords[tx.data["to"]].append(tx.data["dateCreated"])

                #Adjust state of transactions
                self.inProcessTransactions.remove(tx)
                self.completedTransactions.append(tx)

            self.blocks.update({index: self.miningJob}) # Persist block to blocks
            self.lastblock =  self.blocks[index]  # Update last block

            self.miningJob = None  # Clear up the job after persist to blocks
            self.createMiningJob() #Create mining job immediately after mining done.
            
            return True, "Congrats! Your mined block has been accepted!" #WIP: Need to pay mining fee for miner here/








