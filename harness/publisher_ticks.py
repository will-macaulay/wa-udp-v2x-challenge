#DO NOT CHANGE THIS FILE

"""
Publisher: sends tick messages over UDP
PORT: 5006
Message format:
{"tick": 1694301000} #tick is a Unix timestamp in ms

"""

import socket
import time
import json

HOST = "127.0.0.1"
PORT = 5006

def now_ms() -> int:
    return int(time.time() * 1000)

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        for i in range(3):
            msg = {
                "tick": now_ms(),
            }
            payload = json.dumps(msg).encode('utf-8')
            sock.sendto(payload, (HOST, PORT))
            print(f"Sent tick: {payload.decode()} to {HOST}:{PORT}", flush=True)
            time.sleep(1)
    except Exception as e:
        print(f"Error sending tick: {e}", flush=True)
    finally:
        sock.close()

if __name__ == "__main__":
    main()
