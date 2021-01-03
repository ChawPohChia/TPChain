TPChain



References:
1) https://www.freecodecamp.org/news/how-to-build-a-web-application-using-flask-and-deploy-it-to-the-cloud-3551c985e492/
2) https://www.activestate.com/blog/how-to-build-a-blockchain-in-python/
3) https://flask-cors.readthedocs.io/en/latest/
4) MI1: Buildng your own Blockchain -Exercises


Transaction Flow:
0) Initialisation with 
   - TotalTPCoin=1,000,000, Balances[40% go to TPChainFoundation, 10% go to Faucet, 50% go to network itself]
   - Pending transaction
   - Rejected transaction
1) Wallet owner triggers transaction, transaction is send to network.
2) Network receives transaction, have an initial check against account balance, if not sufficent fund then move 
   transaction as rejected transaction, with reason stated
3) If initial checking ok, move transaction into pending transaction.
4) While selected to be inside mining block, double check against balance again, txs waiting for mining into block
   if not sufficent fund then move pending transaction as rejected transaction, with reason stated
4) if mining completed, transaction inside blocks are removed from pending transactions into completed transactions with filled in block index, 
   balances adjusted
5) next round..
