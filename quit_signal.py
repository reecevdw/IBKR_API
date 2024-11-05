from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import threading
import time

class TradeApp(EWrapper, EClient): 
    def __init__(self): 
        EClient.__init__(self, self)

    def error(self, reqId, errorCode, errorString, advancedOrderRejectJson=None):
        print(f"Error {reqId}, Code: {errorCode}, Message: {errorString}")

    def updateAccountValue(self, key: str, val: str, currency: str, accountName: str):
        print(f"Account Update - Key: {key}, Value: {val}, Currency: {currency}, Account Name: {accountName}")

    def updatePortfolio(self, contract: Contract, position: float, marketPrice: float, marketValue: float,
                        averageCost: float, unrealizedPNL: float, realizedPNL: float, accountName: str):
        print(f"UpdatePortfolio - Symbol: {contract.symbol}, SecType: {contract.secType}, Exchange: {contract.exchange}")
        print(f"Position: {position}, MarketPrice: {marketPrice}, MarketValue: {marketValue}")
        print(f"AverageCost: {averageCost}, UnrealizedPNL: {unrealizedPNL}, RealizedPNL: {realizedPNL}")
        print(f"AccountName: {accountName}\n")

    def updateAccountTime(self, timeStamp: str):
        print(f"UpdateAccountTime - Time: {timeStamp}")

    def accountDownloadEnd(self, accountName: str):
        print(f"AccountDownloadEnd - Account: {accountName}")

# Function to listen for "quit" command in a separate thread
def listen_for_quit(app, quit_event):
    while not quit_event.is_set():
        command = input("Enter 'quit' to stop the program: ").strip().lower()
        if command == "quit":
            print("Quitting the program...")
            quit_event.set()
            app.disconnect()

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

# Allow time for connection to establish
time.sleep(1)

# Request account updates (including portfolio data) for the specified account ID
app.reqAccountUpdates(True, account_id)

# Set up the quit event and start the thread for quit command
quit_event = threading.Event()
quit_thread = threading.Thread(target=listen_for_quit, args=(app, quit_event), daemon=True)
quit_thread.start()

# Run the application to keep receiving data until "quit" is entered
while not quit_event.is_set():
    app.run()  # This will continue running until app.disconnect() is called by the quit command