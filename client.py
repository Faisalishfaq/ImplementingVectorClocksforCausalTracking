# client.py
"""
Client with Vector Clock Propagation
------------------------------------
This client:
1. Maintains its own vector clock
2. Before sending request: increments its clock
3. Sends clock + payload to server
4. After response: merges server clock into its own
"""

import requests
from vector_clock import VectorClock

class Client:
    def __init__(self, client_id, server_url):
        self.client_id = client_id
        self.server_url = server_url
        self.vc = VectorClock(client_id)

    def send(self, payload):
        print(f"\n[CLIENT {self.client_id}] Before send: {self.vc.to_dict()}")

        # Step 1: increment before sending
        self.vc.increment(self.client_id)
        print(f"[CLIENT {self.client_id}] After increment: {self.vc.to_dict()}")

        # Step 2: send request to server
        response = requests.post(
            f"{self.server_url}/rpc",
            json={"node_id": self.client_id, "clock": self.vc.to_dict(), "payload": payload}
        )

        server_data = response.json()
        server_clock = server_data["server_clock"]

        print(f"[CLIENT {self.client_id}] Received from server: {server_clock}")

        # Step 3: merge server clock
        self.vc.update(server_clock)
        print(f"[CLIENT {self.client_id}] After merge: {self.vc.to_dict()}")

        return server_data

if __name__ == "__main__":
    # Example demo
    SERVER_URL = "http://127.0.0.1:8080"  # Local testing, change for Railway
    clientA = Client("A", SERVER_URL)

    # Send multiple requests
    clientA.send("Hello from A - 1")
    clientA.send("Hello from A - 2")
