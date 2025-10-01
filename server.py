# server.py
"""
Assignment: Implementing Vector Clocks for Causal Tracking
----------------------------------------------------------
This server:
1. Accepts requests with vector clock metadata
2. Updates its own local vector clock
3. Returns the updated vector clock in the response

? Requirements satisfied:
- Step 2: RPC Server with Vector Clock
- Step 4 (part): Server logs show causality with each request
"""

import os
from flask import Flask, request, jsonify
from vector_clock import VectorClock
from datetime import datetime
import socket

# Utility function to print timestamp
def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Flask App
app = Flask(__name__)

# Server initialization
SERVER_ID = "S"   # Server acts like one logical node
server_vc = VectorClock(SERVER_ID)

# -------- Root endpoint (for browser testing) --------
@app.route("/", methods=["GET"])
def home():
    """Simple GET to check if server is running"""
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return {
        "message": "? Vector Clock RPC Server is running",
        "server_id": SERVER_ID,
        "server_ip": ip,
        "endpoints": {
            "/": "GET ? This message",
            "/rpc": "POST ? Send vector clock + payload"
        }
    }

# -------- RPC endpoint --------
@app.route("/rpc", methods=["POST"])
def rpc():
    """
    Handles client requests:
    - Reads vector clock and payload
    - Updates server clock
    - Returns new server clock
    """

    # Extract JSON
    data = request.get_json(force=True)
    client_id = data.get("node_id", "unknown")
    client_clock = data.get("clock", {})
    payload = data.get("payload", "")

    # Display incoming request
    client_ip = request.remote_addr
    print(f"\n[{now()}] [SERVER] ?? Request received")
    print(f"    From Client: {client_id} ({client_ip})")
    print(f"    Payload    : {payload}")
    print(f"    Client VC  : {client_clock}")

    # Step 1: Merge client clock into server's clock
    server_vc.update(client_clock)

    # Step 2: Increment server clock for "processing event"
    server_vc.increment(SERVER_ID)

    # Display updated clock
    print(f"[{now()}] [SERVER] ?? Updated Server VC: {server_vc.to_dict()}")

    # Return response JSON
    return jsonify({
        "server_id": SERVER_ID,
        "server_clock": server_vc.to_dict(),
        "received_from": client_id,
        "payload_echo": payload,
        "timestamp": now()
    })

# -------- Entry Point --------
if __name__ == "__main__":
    # Railway / Render / Local default ? port 8080
    port = int(os.environ.get("PORT", 8080))
    print(f"[{now()}] ?? Server starting on 0.0.0.0:{port} (SERVER_ID={SERVER_ID})")
    app.run(host="0.0.0.0", port=port)
