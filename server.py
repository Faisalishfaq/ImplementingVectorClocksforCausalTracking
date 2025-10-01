# server.py
from flask import Flask, request, jsonify
from vector_clock import VectorClock
import threading

app = Flask(__name__)

server_id = "S"
server_vc = VectorClock(node_id=server_id)
lock = threading.Lock()

@app.route("/rpc", methods=["POST"])
def rpc():
    data = request.get_json(force=True)
    client_id = data.get("node_id")
    client_clock = data.get("clock", {})
    payload = data.get("payload", None)

    with lock:
        app.logger.info(f"[SERVER] Received from {client_id} | client_clock={client_clock} | payload={payload}")

        server_vc.update(client_clock)
        server_vc.increment(server_id)

        app.logger.info(f"[SERVER] Updated server clock: {server_vc.to_dict()}")

        return jsonify({
            "clock": server_vc.to_dict(),
            "reply": f"Handled by server {server_id}"
        }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
