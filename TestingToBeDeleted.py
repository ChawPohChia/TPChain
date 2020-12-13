## testing to filrer python list
from Transaction import Transaction
import copy
import datetime

"""
#'{"from":"1Nh1qKQQ7q8Etsu5QndtQUkDHk5oiv8zKr","to":"XxnoCyJMtY323Y7mG6ePWtAmCoTH7KGqxX","value":100000,"fee":100,"dateCreated":"2020-12-13 16:27:34"}'
def strToDatetime(dateString):
    return datetime.datetime.strptime(dateString, '%Y-%m-%d %H:%M:%S')

t1=Transaction(data={"from":"1Nh1qKQQ7q8Etsu5QndtQUkDHk5oiv8zKr","to":"XxnoCyJMtY323Y7mG6ePWtAmCoTH7KGqxX","value":100000,"fee":100,"dateCreated":"2020-12-13 18:27:34"}, senderPubKey="", transactionDataHash="",senderSignature="")
t2=Transaction(data={"from":"2Nh1qKQQ7q8Etsu5QndtQUkDHk5oiv8zKr","to":"XxnoCyJMtY323Y7mG6ePWtAmCoTH7KGqxX","value":100000,"fee":100,"dateCreated":"2020-12-13 17:27:34"}, senderPubKey="", transactionDataHash="",senderSignature="")
t3=Transaction(data={"from":"3Nh1qKQQ7q8Etsu5QndtQUkDHk5oiv8zKr","to":"XxnoCyJMtY323Y7mG6ePWtAmCoTH7KGqxX","value":100000,"fee":100,"dateCreated":"2020-12-13 16:27:34"}, senderPubKey="", transactionDataHash="",senderSignature="")
t4=Transaction(data={"from":"4Nh1qKQQ7q8Etsu5QndtQUkDHk5oiv8zKr","to":"XxnoCyJMtY323Y7mG6ePWtAmCoTH7KGqxX","value":100000,"fee":100,"dateCreated":"2020-12-13 17:27:34"}, senderPubKey="", transactionDataHash="",senderSignature="")
t5=Transaction(data={"from":"4Nh1qKQQ7q8Etsu5QndtQUkDHk5oiv8zKr","to":"XxnoCyJMtY323Y7mG6ePWtAmCoTH7KGqxX","value":100000,"fee":100,"dateCreated":"2020-12-13 16:27:34"}, senderPubKey="", transactionDataHash="",senderSignature="")
t6=Transaction(data={"from":"4Nh1qKQQ7q8Etsu5QndtQUkDHk5oiv8zKr","to":"XxnoCyJMtY323Y7mG6ePWtAmCoTH7KGqxX","value":100000,"fee":100,"dateCreated":"2020-12-13 12:27:34"}, senderPubKey="", transactionDataHash="",senderSignature="")
t7=Transaction(data={"from":"2Nh1qKQQ7q8Etsu5QndtQUkDHk5oiv8zKr","to":"XxnoCyJMtY323Y7mG6ePWtAmCoTH7KGqxX","value":100000,"fee":100,"dateCreated":"2020-11-13 13:27:34"}, senderPubKey="", transactionDataHash="",senderSignature="")

pendingTransactions=[t1,t2,t3,t4,t5,t6,t7]
uniqueTransactions=[]
for ptx in pendingTransactions:
    toSkip = False;
    for element in pendingTransactions:
        if ((ptx.data["from"] == element.data["from"]) & (strToDatetime(ptx.data["dateCreated"]) > strToDatetime(element.data["dateCreated"]))):
            toSkip=True;
    if (not toSkip):
        uniqueTransactions.append(ptx)

for tx in uniqueTransactions:
   pendingTransactions.remove(tx)

print("Checking..")
"""

"""
pendingTransactions=[t1,t2,t3,t4,t5, t6, t7]
TransToProcess=[]
#pendingTransactions_Temp=copy.deepcopy(pendingTransactions)
TransToProcess.append(pendingTransactions[0])
#pendingTransactions.remove(TransToProcess[0])


for ptx in pendingTransactions:
    for ttp in TransToProcess: # checking this pending transaction is with same name in ttp
        # Only one "from" address's transaction in one block, if more, only allow the earliest
        if((ptx.data["from"]==ttp.data["from"])):
            if (strToDatetime(ptx.data["dateCreated"]) < strToDatetime(ttp.data["dateCreated"])):
                TransToProcess.append(ptx)
                #pendingTransactions.append(ttp)
                TransToProcess.remove(ttp)
            else:
                continue
    if ptx not in TransToProcess:
        TransToProcess.append(ptx)
    #pendingTransactions.remove(ptx)

for tx in TransToProcess:
   pendingTransactions.remove(tx)
"""





