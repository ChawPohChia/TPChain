from flask import Flask, request
from Node import Node
import sys
import random
import socket
from flask_cors import CORS, cross_origin
from http import HTTPStatus
from Transaction import Transaction
from flask import jsonify
import json
from datetime import datetime as dt

app = Flask(__name__)
CORS(app)

@app.route("/")
def welcome():
    return "<h1>Welcome to TP Chain！！" \
           "<h2>Thank you for Starting a TP Node~</h1>"

@app.route("/connectedNodeInfo")
def returnNodeInfo():
    nodeInfo = {"NodeID": runningNode.NodeID,
                "NodeURL": runningNode.SelfURL}
    return nodeInfo

@app.route("/networkInfo")
def returnNetworkInfo():
    networkInfo = { "TotalBlockNumber:": len(runningNode.Chain.blocks),
                   "Difficulty": runningNode.Chain.Difficulty,
                   "TPFoundationWalletAddress": runningNode.Chain.TPFoundationWalletAddress,
                   "TPFaucetWalletAddress": runningNode.Chain.FaucetAddress,
                   "TotalSupplyTPCoin": runningNode.Chain.TotalTPCoin,
                   "TPCoinBalance:": runningNode.Chain.NetworkCoinBalance}
    return networkInfo


@app.route("/debug")
def debugNode():
    debugInfo = {"node": {"nodeId": "175eb5a5de21374b2747382b", "host": "localhost", "port": "20801",
                          "selfUrl": "http://localhost:20801", "peers": {}, "chain": {"blocks": [{"index": 0,
                                                                                                  "transactions": [{
                                                                                                                       "from": "0000000000000000000000000000000000000000",
                                                                                                                       "to": "f3a1e69b6176052fcc4a3248f1c5a91dea308ca9",
                                                                                                                       "value": 1000000000000,
                                                                                                                       "fee": 0,
                                                                                                                       "dateCreated": "2018-01-01T00:00:00.000Z",
                                                                                                                       "data": "genesis tx",
                                                                                                                       "senderPubKey": "00000000000000000000000000000000000000000000000000000000000000000",
                                                                                                                       "transactionDataHash": "8a684cb8491ee419e7d46a0fd2438cad82d1278c340b5d01974e7beb6b72ecc2",
                                                                                                                       "senderSignature": [
                                                                                                                           "0000000000000000000000000000000000000000000000000000000000000000",
                                                                                                                           "0000000000000000000000000000000000000000000000000000000000000000"],
                                                                                                                       "minedInBlockIndex": 0,
                                                                                                                       "transferSuccessful": true}],
                                                                                                  "difficulty": 0,
                                                                                                  "minedBy": "0000000000000000000000000000000000000000",
                                                                                                  "blockDataHash": "15cc5052fb3c307dd2bfc6bcaa057632250ee05104e4fb7cc75e59db1a92cefc",
                                                                                                  "nonce": 0,
                                                                                                  "dateCreated": "2018-01-01T00:00:00.000Z",
                                                                                                  "blockHash": "c6da93eb4249cb5ff4f9da36e2a7f8d0d61999221ed6910180948153e71cc47f"}],
                                                                                      "pendingTransactions": [],
                                                                                      "currentDifficulty": 5,
                                                                                      "miningJobs": {}},
                          "chainId": "c6da93eb4249cb5ff4f9da36e2a7f8d021.00d61999221ed6910180948153e71cc47f"},
                 "config": {"defaultServerHost": "localhost", "defaultServerPort": 5555,
                            "faucetPrivateKey": "838ff8634c41ba62467cc874ca156830ba55efe3e41ceeeeae5f3e77238f4eef",
                            "faucetPublicKey": "8c4431db61e9095d5794ff53a3ae4171c766cadef015f2e11bec22b98a80f74a0",
                            "faucetAddress": "f3a1e69b6176052fcc4a3248f1c5a91dea308ca9",
                            "nullAddress": "0000000000000000000000000000000000000000",
                            "nullPubKey": "00000000000000000000000000000000000000000000000000000000000000000",
                            "nullSignature": ["0000000000000000000000000000000000000000000000000000000000000000",
                                              "0000000000000000000000000000000000000000000000000000000000000000"],
                            "startDifficulty": 5, "minTransactionFee": 10, "maxTransactionFee": 1000000,
                            "blockReward": 5000000, "maxTransferValue": 10000000000000, "safeConfirmCount": 3,
                            "genesisBlock": {"index": 0, "transactions": [
                                {"from": "0000000000000000000000000000000000000000",
                                 "to": "f3a1e69b6176052fcc4a3248f1c5a91dea308ca9", "value": 1000000000000, "fee": 0,
                                 "dateCreated": "2018-01-01T00:00:00.000Z", "data": "genesis tx",
                                 "senderPubKey": "00000000000000000000000000000000000000000000000000000000000000000",
                                 "transactionDataHash": "8a684cb8491ee419e7d46a0fd2438cad82d1278c340b5d01974e7beb6b72ecc2",
                                 "senderSignature": ["0000000000000000000000000000000000000000000000000000000000000000",
                                                     "0000000000000000000000000000000000000000000000000000000000000000"],
                                 "minedInBlockIndex": 0, "transferSuccessful": true}], "difficulty": 0,
                                             "minedBy": "0000000000000000000000000000000000000000",
                                             "blockDataHash": "15cc5052fb3c307dd2bfc6bcaa057632250ee05104e4fb7cc75e59db1a92cefc",
                                             "nonce": 0, "dateCreated": "2018-01-01T00:00:00.000Z",
                                             "blockHash": "c6da93eb4249cb5ff4f9da36e2a7f8d0d61999221ed6910180948153e71cc47f"}},
                 "confirmedBalances": {"0000000000000000000000000000000000000000": -1000000000000,
                                       "f3a1e69b6176052fcc4a3248f1c5a91dea308ca9": 1000000000000}}
    return debugInfo


@app.route("/debug/reset-chain")
def resetChain():
    resetChainInfo = {"message": "The chain was reset to its genesis block"}
    return resetChainInfo


@app.route("/debug/mine/<minerAddress>/<difficulty>")
def getMinerDifficulty(minerAddress, difficulty):
    minerDifficulty = "Miner at address " + minerAddress + " difficulty is " + difficulty
    return minerDifficulty

@app.route("/mining/get-mining-job")
def getMiningJob():
    tx = request.values['Miner']
    minerAddress= tx
    print("Mining request comes in, "+minerAddress+" request for a job." )
    miningJob=runningNode.Chain.getMiningJob()
    return miningJob

@app.route("/mining/submit-mined-block", methods=['POST'])
@cross_origin()
def receiveMinedBlock(): # minedBlock={'MinedBy':MinerIP,"Blockindex":miningDict["Index"], "MinedNonce":str(mining.nonce)}
    MinedBy = request.values["MinedBy"]
    BlockIndex = int(request.values["Blockindex"]) #request change this value to string, need to change back to int
    MinedNonce = request.values["MinedNonce"]
    accepted, msg = runningNode.Chain.verifyAndSubmitBlock(BlockIndex,MinedNonce, MinedBy)
    return {"accepted":accepted,"message":msg}

@app.route("/block/latest")
def getLatestBlock():
    print("Retriving latest block info...")
    lastblock = json.dumps(runningNode.Chain.lastblock, default=lambda o: o.__dict__,sort_keys=True, indent=4)
    return lastblock

@app.route("/block/all")
def getAllBlocks():
    print("Retriving all block transaction...")
    allBlocksList=[{"Block "+str(key):dumpBlockToJson(runningNode.Chain.blocks[key])} for key in runningNode.Chain.blocks.keys()]
    allBlocks = json.dumps([blk for blk in allBlocksList])
    return allBlocks

def dumpBlockToJson(block):
    return json.dumps(block, default=lambda o: o.__dict__)

@app.route("/block/latestBlockTransaction")
def getLatestBlockTxs():
    print("Retriving latest block transaction...")
    latestBlockTxs = json.dumps([ob.__dict__ for ob in runningNode.Chain.lastblock.transactions])
    return latestBlockTxs

@app.route("/block/<id>")
def getBlockWithID(id):
    print("Retriving Block info with Id:" + id)
    blockInfo = "Index:" + id
    return blockInfo

@app.route("/transactions/pending")
def getPendingTransaction():
    pendingTransactionsJson = json.dumps([ob.__dict__ for ob in runningNode.Chain.pendingTransactions])    
    return pendingTransactionsJson

@app.route("/transactions/inprocess")
def getInProcessTransaction():
    inProcessTransactionsJson = json.dumps([ob.__dict__ for ob in runningNode.Chain.inProcessTransactions])
    return inProcessTransactionsJson

@app.route("/transactions/completed")
def getCompletedTransaction():
    completedTransactionsJson = json.dumps([ob.__dict__ for ob in runningNode.Chain.completedTransactions])
    return completedTransactionsJson

@app.route("/transactions/rejected")
def getRejectedTransaction():
    rejectedTransactionsJson = json.dumps([ob.__dict__ for ob in runningNode.Chain.rejectedTransactions])
    return rejectedTransactionsJson

@app.route("/transactions/confirmed")
def getConfirmedTransaction():
    confirmedTransactions = "This is confirmed transactions results."
    return confirmedTransactions

@app.route("/transactions/<tranHash>")
def getTransaction(tranHash):
    print("Retriving transaction info with Id:" + tranHash)
    tranInfo = "Transaction Hash:" + tranHash
    return tranInfo

@app.route("/transactions/send", methods=['POST'])
@cross_origin()
def receiveTransaction():
    tx = request.form

    #Data: {"from": "1Asq3p1PdSW39sRWSceiPDP5uTmrYawESW", "to": "XxnoCyJMtY323Y7mG6ePWtAmCoTH7KGqxX", "value": 100000,
    #       "fee": 100, "dateCreated": "2020-12-1 16:4:38"}
    #SenderPubKey: This is sender PubKey
    #TransactionDataHash: �`���o�B�_Q��:-_J�g q > J�7�Gh"
    # SenderSignature: 48, 68, 2, 32, 17, 222, 44, 1, 98, 161, 16, 33, 52, 31, 54, 11, 129, 235, 136, 253, 23, 40, 8, 224, 153, 93, 194, 211, 215, 185, 208, 67, 174, 101, 182, 48, 2, 32, 68, 113, 81, 75, 48, 174, 101, 44, 96, 241, 9, 19, 138, 68, 248, 202, 149, 213, 86, 11, 63, 234, 134, 189, 17, 178, 116, 54, 94, 86, 161, 127
    # DER encoding of an ECDSA signature: 70 bytes insides

    data = json.loads(tx['data'])
    #WIP: Need to verify received transaction here..
    receivedTransaction= Transaction(data, tx['senderPubKey'], tx['transactionDataHash'], tx['senderSignature'])
    runningNode.Chain.addTransaction(receivedTransaction)
    print(receivedTransaction)
    return "200"

@app.route("/faucet/request", methods=['POST'])
@cross_origin()
def requestCoin():
    tx = request.form
    #Data: {"from": "1Asq3p1PdSW39sRWSceiPDP5uTmrYawESW", "to": "XxnoCyJMtY323Y7mG6ePWtAmCoTH7KGqxX", "value": 100000,
    #       "fee": 100, "dateCreated": "2020-12-1 16:4:38"}
    data = json.loads(tx['data'])
    currentRequestDateTime = dt.now().strftime("%Y-%m-%d %H:%M:%S")
    #GreedinessChecking
    isGreedy=runningNode.Chain.checkFaucetRequestGreediness(data["to"],currentRequestDateTime)
    if(isGreedy):
        return {"accepted":False,"message":"Your last request for this account is less than 24 hours."}
    
    ##Network itself to complete faucet transaction info
    data["from"] = runningNode.Chain.FaucetAddress
    data["value"] = runningNode.Chain.FaucetRequestAmount
    data["fee"] = 0
    data["dateCreated"]=currentRequestDateTime

    coinRequestTransaction= Transaction(data, "","","");
    #Verify transaction
    isVerifiedSuccesfully= runningNode.Chain.verifyTransaction(coinRequestTransaction);
    if(not isVerifiedSuccesfully):
        return {"accepted":False,"message":coinRequestTransaction.remarks}

    runningNode.Chain.addTransaction(coinRequestTransaction)
    ##WIP: when request is mined, need to add in the historical request record.
    return  {"accepted":True,"message":"Your request is accepted and is in mining process."}

@app.route("/address/<address>/transactions")
def getAddressTransactions(address):
    (numberofTransactions, transactions)=runningNode.Chain.checkAccountTransactions(address);
    if(numberofTransactions<=0):
        return {"numberofTransactions": numberofTransactions, "Transactions": transactions}
    else:
        relevantTransactionsJson = json.dumps([tx.__dict__ for tx in transactions])
        return {"numberofTransactions":numberofTransactions,"Transactions":relevantTransactionsJson}

@app.route("/address/<address>/balance")
def getAddressBalance(address):
    (balance, msg) = runningNode.Chain.checkAccountBalance(address);
    return {"balance": balance, "message": msg}

@app.route("/peers")
def getPeers():
    peersInfo = "These are peers info"
    return peersInfo

#let user set the nodeID and port while running the node
if __name__ == "__main__":
    """
    if len(sys.argv) == 2:
        nodeID = sys.argv[1]
        nodePort = sys.argv[2]
    else:
        nodeID = "xxxx001"
        nodePort=random.randint(1000, 9999)
        """
    #nodePort = random.randint(1000, 9999)
    nodePort = 1234
    nodeID = "TPChainNode_"+str(nodePort)
    nodeURL= "127.0.0.1:"+str(nodePort);
    runningNode = Node(nodeID, nodeURL)
    app.run(port=nodePort)

