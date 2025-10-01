# server.py
"""
RPC Server with Vector Clock
----------------------------
This Flask server:
1. Accepts POST requests with vector clock metadata
2. Updates its own vector clock
3. Returns updated vector clock in response
"""

import os
from flask import Flask, request, jsonify
from vector_clock import VectorClock

app = Flask(__name__)

# Server node setup
SERVER_ID = "S"
server_vc = VectorClock(SERVER_ID)

@app.route("/", methods=["GET"])
def home():
    """Default route (for browser testing)."""
    return {
        "message": "Vector Clock RPC Server is running ✅",
        "usage": "Send POST request to /rpc with JSON body"
    }

@app.route("/rpc", methods=["POST"])
def rpc():
    """Handle RPC request with vector clocks."""
    data = request.get_json(force=True)

    client_id = data.get("node_id", "unknown")
    client_clock = data.get("clock", {})
    payload = data.get("payload", "")

    print(f"[SERVER] Received from {client_id} | client_clock={client_clock} | payload={payload}")

    # Merge client clock into server clock
    server_vc.update(client_clock)
    # Increment server clock for this event
    server_vc.increment(SERVER_ID)

    print(f"[SERVER] Updated server clock: {server_vc.to_dict()}")

    return jsonify({
        "server_id": SERVER_ID,
        "server_clock": server_vc.to_dict(),
        "message": f"Processed request from {client_id}",
        "payload_echo": payload
    })

if __name__ == "__main__":
    # Railway sets PORT env variable automatically
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
