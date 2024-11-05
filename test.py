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

# Step 2: Connect to TWS or IB Gateway
def run_loop():
    app.run()

app = IBKRClient()
app.connect("127.0.0.1", 7497, clientId=1)  # Use 7496 for live trading

# Step 3: Start a Thread
api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()

# Step 4: Request Account Summary
time.sleep(1)  # Allow time to establish connection
app.reqAccountSummary(1, "All", "$LEDGER")

# Step 5: Disconnect
time.sleep(5)  # Adjust this to keep the connection alive for as long as needed
app.disconnect()