from hashlib import sha256
import datetime

def getBlockHash(blockString, nonce):
    return sha256((blockString + str(nonce)).encode()).hexdigest()

def verifyBlockHash(blockString, nonce, difficulty):
    blockHash = getBlockHash(blockString, nonce)
    if (blockHash.startswith('0' * difficulty)):
        return True, blockHash, "Block is verified! Block was mined successfull with nonce: "+str(nonce)
    else:
        return False, blockHash, "Block nonce: " + str(nonce) +" is INCORRECT for this block, please try to mine again"

def strToDatetime(dateString):
    return datetime.datetime.strptime(dateString, '%Y-%m-%d %H:%M:%S')
