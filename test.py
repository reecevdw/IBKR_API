from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import threading
import time

# Step 1: Create the Connection Class
class IBKRClient(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def error(self, reqId, errorCode, errorString, advancedOrderRejectJson=None):
        print(f"Error {reqId}, Code: {errorCode}, Message: {errorString}")

    def accountSummary(self, reqId, account, tag, value, currency):
        print(f"Account: {account}, {tag}: {value} {currency}")

    # Step 1b: Add a method to handle tick price data
    def tickPrice(self, reqId, tickType, price, attrib):
        print(f"Tick Price. Ticker Id: {reqId}, Tick Type: {tickType}, Price: {price}")

    def tickSize(self, reqId, tickType, size):
        print(f"Tick Size. Ticker Id: {reqId}, Tick Type: {tickType}, Size: {size}")

# Step 2: Connect to TWS or IB Gateway
def run_loop():
    app.run()

app = IBKRClient()
app.connect("127.0.0.1", 7497, clientId=1)  # Use 7496 for live trading

# Step 3: Start a Thread
api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()

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
app.reqMktData(1, create_stock_contract("TQQQ"), "", False, False, [])

# Step 6: Request Account Summary (Optional)
app.reqAccountSummary(1, "All", "$LEDGER")

# Keep the script running to receive data
time.sleep(20)  # Adjust this to keep the connection open as long as needed
app.disconnect()