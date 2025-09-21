#Author: Will Macaulay
#Date: 09/21/2025
#This should be the only file you edit. You are free to look at other files for reference, but do not change them.
#Below are are two methods which you must implement: euclidean_dist_to_origin and nearest_neighbor as well as the main function beacon handling. 
#Helper Functions are allowed, but not required. You must not change the imports, the main function signature, or the return value of the main function.


"""
Neighbor Table

Listen on UDP 127.0.0.1:5005 for beacon messages:
  {"id":"veh_XXX","pos":[x,y],"speed":mps,"ts":epoch_ms}

Collect beacons for ~1 second starting from the *first* message.
Then print exactly ONE JSON line and exit:

{
  "topic": "/v2x/neighbor_summary",
  "count": <int>,
  "nearest": {"id": "...", "dist": <float>} OR null,
  "ts": <now_ms>
}

Constraints:
- Python 3 stdlib only.
- Ignore malformed messages; don’t crash.
- Do NOT listen to ticks (5006).
"""

import socket, json, time, math, sys
from typing import Dict, Any, Optional, Tuple

HOST = "127.0.0.1"
PORT_BEACON = 5005
COLLECT_WINDOW_MS = 1000  # ~1 second

def now_ms() -> int:
    return int(time.time() * 1000)



# nearest_neighbors already deals with errors, included error handling anyways just cause

def euclidean_dist_to_origin(pos) -> float:

    # verifying that pos is a list/tuple
    if not isinstance(pos, (list, tuple)):
        raise TypeError('position must be a list or tuple')
    
    # verifying that pos has length 2
    if len(pos) != 2:
        raise TypeError('position must be of length 2')
    
    # verifying that pos elements are numbers
    try:
        x = float(pos[0])
        y = float(pos[1])
    except (TypeError, ValueError):
        raise TypeError('position must contain numbers')
    
    # calculation
    return math.sqrt(x**2 + y**2)



def nearest_neighbor(neighbors: Dict[str, Dict[str, Any]]) -> Optional[Tuple[str, float]]:

    min_id = None
    min_dist = math.inf

    # find neighbor with smallest distance, ignore invalid neighbors/positions
    for n in neighbors:
        try:
            curr_dist = euclidean_dist_to_origin(neighbors[n]["pos"])
            if curr_dist < min_dist:
                min_id = n
                min_dist = curr_dist
        except:
            continue

    # return tuple with id and distance, or none if no distances are found
    return (min_id, min_dist) if min_id is not None else None



# function for checking if msg is valid, then modifying the dictionary of neighbors
# this method is called for every beacon message published by other cars (in this case the harness)
# their message is broadcast blindly, they don't need to know who's receiving it
# the message is received by us and all other subscribers when we open a socket and decode msg's from bytes to utf-8 text
# the msg parameter is one decoded message that a publisher is broadcasting, obtained from the current call of recvfrom
# the neighbors parameter contains a reference to the neighbors dictionary in main()
# this method will continue to be called until the socket times out or closes after the set duration (~1 second)

def is_msg_valid(msg, neighbors):

    expected_types = {'id': str, 'pos': (list, tuple), 'speed': float, 'ts': int}

    for key in msg:
        # check if key in msg isn't supposed to be there
        if key not in expected_types.keys():
            return
        
        # check if value type in msg isn't correct for its key
        if not isinstance(msg[key], expected_types[key]):
            return
        
    for expected_key in expected_types:
        # check if expected key isn't in msg
        if expected_key not in msg.keys():
            return
        
    # for pos, check length and if elements are numbers
    if len(msg["pos"]) != 2:
        return
    
    if not isinstance(msg["pos"][0], (int, float)) or not isinstance(msg["pos"][1], (int, float)):
        return
    

    # set neighbor if all is well
    neighbors[msg["id"]] = {"pos": msg["pos"], "speed": msg["speed"], "last_ts": msg["ts"]}



def main() -> int:
    neighbors: Dict[str, Dict[str, Any]] = {}
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT_BEACON))
    sock.settimeout(1.5) 

    first_ts: Optional[int] = None
    try:
        while True:
            try:
                data, _ = sock.recvfrom(4096)
            except socket.timeout:
                break  

            try:
                msg = json.loads(data.decode("utf-8"))
            except json.JSONDecodeError:
                continue  
            #TODO block
            

            # see function above for comments on process
            is_msg_valid(msg, neighbors)


            #END of TODO block
            now = now_ms()
            if first_ts is None:
                first_ts = now
            # stop after ~1 second from first message
            if first_ts is not None and (now - first_ts) >= COLLECT_WINDOW_MS:
                break

    finally:
        sock.close()

    # Build summary
    nn = nearest_neighbor(neighbors)
    summary = {
        "topic": "/v2x/neighbor_summary",
        "count": len(neighbors),
        "nearest": None if nn is None else {"id": nn[0], "dist": nn[1]},
        "ts": now_ms(),
    }
    print(json.dumps(summary), flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())
