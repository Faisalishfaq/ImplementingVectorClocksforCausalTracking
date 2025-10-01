# client.py
"""
Assignment: Implementing Vector Clocks for Causal Tracking
----------------------------------------------------------
This client:
1. Maintains its own vector clock
2. Before sending request → increments local clock
3. Attaches vector clock + payload in request
4. After response → merges server's clock into local clock
"""

import requests
from datetime import datetime
from vector_clock import VectorClock

# Utility for timestamp
def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ---------- Client Setup ----------
CLIENT_ID = "A"   # you can make B, C, etc. for multiple clients
client_vc = VectorClock(CLIENT_ID)

# Change this URL according to deployment
SERVER_URL = "http://127.0.0.1:8080/rpc"
# Example for Railway after deploy:
# SERVER_URL = "https://your-app-name.up.railway.app/rpc"

# ---------- Function: send request ----------
def send_request(payload):
    print(f"\n[{now()}] [CLIENT {CLIENT_ID}] 📤 Preparing request...")

    # Step 1: Increment local clock
    client_vc.increment(CLIENT_ID)
    print(f"[{now()}] [CLIENT {CLIENT_ID}] ⏱ Local clock after increment: {client_vc.to_dict()}")

    # Step 2: Create JSON payload
    data = {
        "node_id": CLIENT_ID,
        "clock": client_vc.to_dict(),
        "payload": payload
    }

    # Step 3: Send POST request
    try:
        response = requests.post(SERVER_URL, json=data)
        response.raise_for_status()
    except Exception as e:
        print(f"[{now()}] [CLIENT {CLIENT_ID}] ❌ Error contacting server: {e}")
        return

    # Step 4: Parse server response
    server_data = response.json()
    server_clock = server_data.get("server_clock", {})
    print(f"[{now()}] [CLIENT {CLIENT_ID}] 📩 Response received from server")
    print(f"    Server VC : {server_clock}")
    print(f"    Payload   : {server_data.get('payload_echo')}")
    print(f"    Timestamp : {server_data.get('timestamp')}")

    # Step 5: Merge server’s clock into client’s clock
    client_vc.update(server_clock)
    print(f"[{now()}] [CLIENT {CLIENT_ID}] 🔄 Updated local clock after merge: {client_vc.to_dict()}")

# ---------- Main ----------
if __name__ == "__main__":
    print(f"🚀 Client {CLIENT_ID} started. Target server: {SERVER_URL}")

    # Example interactions
    send_request("Hello from Client A (1st request)")
    send_request("Another message from Client A (2nd request)")
