# server.py
import os
from flask import Flask, request, jsonify
from vector_clock import VectorClock
from datetime import datetime
import socket

def now():
    return datetime.now().strftime("%H:%M:%S")

app = Flask(__name__)

SERVER_ID = "S"
server_vc = VectorClock(SERVER_ID)

# ---------- Default GET route for browser ----------
@app.route("/", methods=["GET"])
def home():
    return {
        "message": "Vector Clock RPC Server is running ✅",
        "endpoint": "/rpc",
        "how_to_use": "Send POST request with JSON body to /rpc"
    }

# ---------- RPC route ----------
@app.route("/rpc", methods=["POST", "GET"])
def rpc():
    if request.method == "GET":
        return {
            "message": "Use POST with JSON body to interact with Vector Clock server",
            "example_body": {
                "node_id": "A",
                "clock": {"A": 1},
                "payload": "Hello from client"
            }
        }

    # POST request (main logic)
    data = request.get_json(force=True)
    client_id = data.get("node_id", "unknown")
    client_clock = data.get("clock", {})
    payload = data.get("payload", "")

    client_ip = request.remote_addr  # IP address of client
    print(f"[{now()}] [SERVER] Received from {client_id} ({client_ip}) "
          f"| client_clock={client_clock} | payload={payload}")

    # merge client clock
    server_vc.update(client_clock)
    # increment server clock for handling event
    server_vc.increment(SERVER_ID)

    print(f"[{now()}] [SERVER] Updated server clock: {server_vc.to_dict()}")

    return jsonify({"clock": server_vc.to_dict()})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Railway provides PORT env var
    app.run(host="0.0.0.0", port=port)
