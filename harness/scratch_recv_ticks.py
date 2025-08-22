#DO NOT CHANGE THIS FILE

"""
Test script to receive ticks on a specific port.
This script listens for UDP packets on port 5006 and prints the received tick data.
"""

import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("127.0.0.1", 5006))
print("Listening for ticks on 127.0.0.1:5006...")
while True:
    data, addr = s.recvfrom(4096)
    print("Got tick from", addr, ":", data.decode())