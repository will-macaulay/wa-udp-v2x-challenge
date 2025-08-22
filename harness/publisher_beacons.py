# DO NOT CHANGE THIS FILE

# harness/publisher_beacons.py
"""
Publisher: sends one or more fake car beacons over UDP.
Port: 5005
Default message (if no env set):
  {"id":"veh_123","pos":[10.0,5.0],"speed":4.0,"ts":<now_ms>}
Environment variables (all optional):
- BEACON_DISABLE="1" -> send nothing and exit
- BEACON_MESSAGES='[{"id":"veh_123","pos":[10,5],"speed":4.0}]'  (JSON list; ts auto-filled)
- BEACON_INTERVAL_MS="50"   delay between messages
- BEACON_SLEEP_BEFORE_MS="1000"  initial delay before first send
"""
import os, socket, json, time

HOST = "127.0.0.1"
PORT = 5005

def now_ms() -> int:
    return int(time.time() * 1000)

def main():
    if os.getenv("BEACON_DISABLE") == "1":
        return

    # Defaults
    msgs = [{"id": "veh_123", "pos": [10.0, 5.0], "speed": 4.0}]
    try:
        if "BEACON_MESSAGES" in os.environ:
            msgs = json.loads(os.environ["BEACON_MESSAGES"])
            assert isinstance(msgs, list)
    except Exception:
        msgs = [{"id": "veh_123", "pos": [10.0, 5.0], "speed": 4.0}]

    interval_ms = int(os.getenv("BEACON_INTERVAL_MS", "50"))
    sleep_before_ms = int(os.getenv("BEACON_SLEEP_BEFORE_MS", "1000"))

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        time.sleep(sleep_before_ms / 1000.0)
        for i, m in enumerate(msgs):
            if "ts" not in m:
                m = {**m, "ts": now_ms()}
            payload = json.dumps(m).encode("utf-8")
            sock.sendto(payload, (HOST, PORT))
            print(f"Sent message: {payload.decode()} to {HOST}:{PORT}", flush=True)
            if i != len(msgs) - 1:
                time.sleep(interval_ms / 1000.0)
    finally:
        sock.close()

if __name__ == "__main__":
    main()