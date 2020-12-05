class Transaction:
    # Received transaction from wallet will be in the following format:
    # Data: {"from": "1Asq3p1PdSW39sRWSceiPDP5uTmrYawESW", "to": "XxnoCyJMtY323Y7mG6ePWtAmCoTH7KGqxX", "value": 100000,
    #       "fee": 100, "dateCreated": "2020-12-1 16:4:38"}
    # SenderPubKey: This is sender PubKey
    # TransactionDataHash: �`���o�B�_Q��:-_J�g q > J�7�Gh"
    # SenderSignature: 48, 68, 2, 32, 17, 222, 44, 1, 98, 161, 16, 33, 52, 31, 54, 11, 129, 235, 136, 253, 23, 40, 8, 224, 153, 93, 194, 211, 215, 185, 208, 67, 174, 101, 182, 48, 2, 32, 68, 113, 81, 75, 48, 174, 101, 44, 96, 241, 9, 19, 138, 68, 248, 202, 149, 213, 86, 11, 63, 234, 134, 189, 17, 178, 116, 54, 94, 86, 161, 127
    # DER encoding of an ECDSA signature: 70 bytes insides
    def __init__(self, data, senderPubKey, transactionDataHash, senderSignature):
        self.data = data
        self.senderPubKey = senderPubKey
        self.transactionDataHash = transactionDataHash
        self.senderSignature = senderSignature
        self.MinedInBlockIndex = None
        self.transferSuccessful = False

    def setTransferSuccessful(self, transferSuccessful):
        self.transferSuccessful = transferSuccessful

    def setMinedInBlockIndex (self, minedBlockIndex ):
        self.MinedInBlockIndex  = minedBlockIndex

