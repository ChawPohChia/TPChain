from hashlib import sha256
import datetime
import string
import random

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



def id_generator(size=24, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
