from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import time

class TradeApp(EWrapper, EClient): 
    def __init__(self): 
        EClient.__init__(self, self) 

    # Account Wide
    def updateAccountValue(self, key: str, val: str, currency: str, accountName: str):
        print("UpdateAccountValue. Key:", key, "Value:", val, "Currency:", currency, "AccountName:", accountName)
    
    # Position Specific
    def updatePortfolio(self, contract: Contract, position: float, marketPrice: float, marketValue: float, averageCost: float, unrealizedPNL: float, realizedPNL: float, accountName: str):
        print("UpdatePortfolio.", "Symbol:", contract.symbol, "SecType:", contract.secType, "Exchange:", contract.exchange, 
              "Position:", position, "MarketPrice:", marketPrice, "MarketValue:", marketValue, 
              "AverageCost:", averageCost, "UnrealizedPNL:", unrealizedPNL, "RealizedPNL:", realizedPNL, 
              "AccountName:", accountName)

    def updateAccountTime(self, timeStamp: str):
        print("UpdateAccountTime. Time:", timeStamp)

    def accountDownloadEnd(self, accountName: str):
        print("AccountDownloadEnd. Account:", accountName)

# Prompt for port and account ID
port = input("Enter the port (default for paper trading is 7497, live trading is 7496): ")
if not port.isdigit():
    print("Invalid port. Using default 7497 for paper trading.")
    port = 7497
else:
    port = int(port)

account_id = input("Enter your account ID (e.g., U123456 for live, DU123456 for paper): ")

# Create and connect to the application
app = TradeApp()      
app.connect("127.0.0.1", port, clientId=1)

time.sleep(1)

# Request account updates using the specified account ID
app.reqAccountUpdates(True, account_id)
app.run()

# Keep the script running to receive data
time.sleep(5)  # Adjust this to keep the connection open as long as needed
app.disconnect()