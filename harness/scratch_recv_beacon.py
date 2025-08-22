#DO NOT CHANGE THIS FILE

"""
Test script to receive beacons on a specific port.
This script listens for UDP packets on port 5005 and prints the received beacon data.
"""
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("127.0.0.1", 5005))
print("Listening for beacons on 127.0.0.1:5005...")
data, addr = s.recvfrom(4096)
print("Got beacon from", addr, ":", data.decode())