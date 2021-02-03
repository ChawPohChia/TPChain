## testing to filrer python list
from Transaction import Transaction
import copy
from datetime import datetime as dt, timedelta

print(dt.now())
#currentRequestDate="2021-02-02 16:4:38"
currentRequestDate=dt.now().strftime("%Y-%m-%d %H:%M:%S")
print("current request time:"+currentRequestDate)
requestRecords = {"abcabc": ["2021-01-31 16:14:39","2021-02-01 23:4:39","2021-02-03 16:4:37", "2021-02-04 03:14:38", "2021-3-31 16:14:39"],"cdecde": ["2020-12-4 16:4:38", "2020-12-5 16:4:38"]}

for date in requestRecords["abcabc"]:
    history= dt.strptime(date, "%Y-%m-%d %H:%M:%S")
    current = dt.strptime(currentRequestDate, "%Y-%m-%d %H:%M:%S")
    print((current-history).days<1)

#requestRecords["abcabc"].append("2020-12-5 16:4:38")


#for date in requestRecords["abcabc"]:
#    print(date)

#Please refer to https://www.programiz.com/python-programming/datetime/strftime
#a = dt.strptime("2013-12-12 16:4:38", "%Y-%m-%d %H:%M:%S")
#b = dt.strptime("2013-10-15", "%Y-%m-%d")
#print(a - b)




