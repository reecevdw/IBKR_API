# One time pull for Account Data

from ibapi.client import *
from ibapi.wrapper import *
from ibapi.contract import Contract
import time

class TradeApp(EWrapper, EClient): 
    def __init__(self): 
        EClient.__init__(self, self) 

    def accountSummary(self, reqId: int, account: str, tag: str, value: str,currency: str):
        print("AccountSummary. ReqId:", reqId, "Account:", account,"Tag: ", tag, "Value:", value, "Currency:", currency)
    
    def accountSummaryEnd(self, reqId: int):
        print("AccountSummaryEnd. ReqId:", reqId)
    
# Prompt for port and account ID
port = input("Enter the port (default for paper trading is 7497, live trading is 7496): ")
if not port.isdigit():
    print("Invalid port. Using default 7497 for paper trading.")
    port = 7497
else:
    port = int(port)

app = TradeApp()      
# Paper Trading Socket
app.connect("127.0.0.1", port, clientId=1)

time.sleep(1)

app.reqAccountSummary(9001, "All", 'NetLiquidation,TotalCashValue,GrossPositionValue')

app.run()

# Keep the script running to receive data
time.sleep(5)  # Adjust this to keep the connection open as long as needed
app.disconnect()