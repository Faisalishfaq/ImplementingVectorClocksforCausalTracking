# client.py
import requests
import json
from vector_clock import VectorClock
import sys
import os

def run_client(node_id, server_url="http://127.0.0.1:5000/rpc"):
    clock_file = f"vc_{node_id}.json"

    if os.path.exists(clock_file):
        with open(clock_file, "r") as f:
            clock_data = json.load(f)
    else:
        clock_data = {}

    vc = VectorClock(node_id=node_id, clock=clock_data)

    print(f"[CLIENT {node_id}] Before send:", vc.to_dict())
    vc.increment(node_id)
    print(f"[CLIENT {node_id}] After increment:", vc.to_dict())

    payload = {"node_id": node_id, "clock": vc.to_dict(), "payload": f"hello from {node_id}"}
    response = requests.post(server_url, json=payload)

    if response.status_code == 200:
        resp_data = response.json()
        print(f"[CLIENT {node_id}] Server response:", resp_data)

        vc.update(resp_data["clock"])
        print(f"[CLIENT {node_id}] After merge:", vc.to_dict())

        with open(clock_file, "w") as f:
            json.dump(vc.to_dict(), f)
    else:
        print(f"[CLIENT {node_id}] Error:", response.text)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python client.py <NodeID>")
    else:
        run_client(sys.argv[1])
