from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import threading
import time

# Step 1: Create the Connection Class
class TradeApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def error(self, reqId, errorCode, errorString, advancedOrderRejectJson=None):
        print(f"Error {reqId}, Code: {errorCode}, Message: {errorString}")

    def accountSummary(self, reqId: int, account: str, tag: str, value: str,currency: str):
        print("AccountSummary. ReqId:", reqId, "Account:", account,"Tag: ", tag, "Value:", value, "Currency:", currency)
    
    def accountSummaryEnd(self, reqId: int):
        print("AccountSummaryEnd. ReqId:", reqId)

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

    # Step 1b: Add a method to handle tick price data
    def tickPrice(self, reqId, tickType, price, attrib):
        print(f"Tick Price. Ticker Id: {reqId}, Tick Type: {tickType}, Price: {price}")

    def tickSize(self, reqId, tickType, size):
        print(f"Tick Size. Ticker Id: {reqId}, Tick Type: {tickType}, Size: {size}")

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

# Set up the quit event and start the thread for quit command
quit_event = threading.Event()
quit_thread = threading.Thread(target=listen_for_quit, args=(app, quit_event), daemon=True)
quit_thread.start()

# Step 4: Define a contract for the stock (e.g., Apple)
def create_stock_contract(symbol):
    contract = Contract()
    contract.symbol = symbol
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"
    return contract

# Step 5: Request Market Data for Apple (AAPL)
time.sleep(1)  # Allow time to establish connection
app.reqMktData(2, create_stock_contract("TQQQ"), "", False, False, [])

# Request Account Summary (Optional)
app.reqAccountSummary(9001, "All", 'NetLiquidation,TotalCashValue,GrossPositionValue')

# Request account updates (including portfolio data) for the specified account ID
app.reqAccountUpdates(True, account_id)

# Run the application to keep receiving data until "quit" is entered
while not quit_event.is_set():
    app.run()  # This will continue running until app.disconnect() is called by the quit command