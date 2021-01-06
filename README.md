TPChain



References:
1) https://www.freecodecamp.org/news/how-to-build-a-web-application-using-flask-and-deploy-it-to-the-cloud-3551c985e492/
2) https://www.activestate.com/blog/how-to-build-a-blockchain-in-python/
3) https://flask-cors.readthedocs.io/en/latest/
4) MI1: Buildng your own Blockchain -Exercises


Transaction Flow:
Tested accounts from TPWallet
-1) 
Faucet Address
Private Key: 5b23f4329c1e8cbe80db9edfffb6b22ca7ff05493e1e1f1ce0dd3f4b29be7a08
Public Key: 03c377bc590d26b54874e7e7667031ce0841e761b9fd397989d5cbab5e88c5c3be
Public Address: 1EmQd4rXvNEoWLKRNSdnb2GP9i5VQwuaEM

TPFoundation Address
Private Key: d174251970457ac24c14e6dc2b85b541de639b1c6988793cfa57ed72fa49f34c
Public Key: 02aa03bdee6a2258963b10be5441864fff4407fc434161c08cc9ce4b4fa24839a5
Public Address: 1AzKmHdg6j8jPA8sNpxc2z7BMsKLCXRp6L

Tested Account1
Private Key: ae723f8ba2a277b2872827fb5e05f1d2689181519cd3d2704421abb9b1bc6265
Public Key: 029894e3f35803a93e877d10a8e5ff396b0c56b28ab8e1dab079eee373305d1c9c
Public Address: 1JuWhQsM5uKA1VH2BSiqiR66twfyxiahqy

Tested Account2
Private Key: 8d49f6ae0f7298a3b79b4b1708263cbde89421d054c94a3a5ff25eece25b778e
Public Key: 02483a2cf63a1b9bce9ac030dbf6711851affb5ddda5d156cb9880c88b1914cd9a
Public Address: 1F5PHZgy28FymfYZ3mE7HsArGTPWcCh3Nt

Tested Account3
Private Key: c0ce6fd31296470982b9dd5bdb0c30aac780d87611142ac39c4f4f707f99feb8
Public Key: 023dda8139636d507ce24c6495580ea0aac2bb335ac54824bd878d43ea9d97dcb0
Public Address: 1D4HA2rWrW7k6ochjTRwuB2SkNh4uZH618
        
0) Initialisation with 
   - TotalTPCoin=1,000,000, Balances[40% go to TPChainFoundation(), 10% go to Faucet(), 50% go to network itself(balance)
   - Pending transactions
   - Rejected transactions
   - Completed transactions
1) Wallet owner triggers transaction, transaction is send to network.
2) Network receives transaction, have an initial check against account balance, if not sufficent fund then move 
   transaction as rejected transaction, with reason stated
3) If initial checking ok, move transaction into pending transaction.
4) While selected to be inside mining block, double check against balance again, txs waiting for mining into block
   if not sufficent fund then move pending transaction as rejected transaction, with reason stated
4) if mining completed, transaction inside blocks are removed from pending transactions into completed transactions with filled in block index, 
   balances adjusted
5) next round..
