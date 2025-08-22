# Wisconsin Autonomous Infrastructure Subteam Coding Challenge ROS2 Simulation 

This coding challenge is designed for us to evaluate what you can bring to the table and an opportunity for you to get some hands on experience with the tools we use on the controls and infrastructure sub-teams. We use ROS2 Humble as our middleware for our modular system to communicate with each other. A good understanding of ROS is vital for our success. While we understand that this might be your first time hearing of ROS, this challenge also aims for us to see how you can learn on the fly, which is an important aspect of being part of this team. The challenge will simulate ROS2 publisher and subscribers system using UDP messages in Python.

## Challenge Descrpiption

In the package `neighbor_node.py` design the methods `euclidean_dist_to_origin` and `nearest_neighbor`. The two methods will make use of the car beacon messages sent. Then add the implementaion `beacon handling` in the main function. 

- `euclidean_dist_to_origin(pos)`
    - Input: 2D position `[x,y]`
    - Output: Distance from the origin (0,0) to that point

- `nearest_neighbor(beacons)`
    - Input: A list of car beacon messages (each containing an ID and position)
    - Output: The nearest neighbor `(ID and distance)`

- `beacon handling`
    - Your node will listen for UDP "beacon messages" that simulate cars broadcasting their position. These will represent the ROS2 output topics in future work.
    - Your node should then have the computed closest vehicle from `nearest_neighbor(beacons)` and publish a summary message in the required output format. 


### euclidean_dist_to_origin
Example:
    Input: pos = [3.0, 4.0]
    Output: 5.0 

### nearest_neighbor(beacons)
Example: 
    Input: neighbors = {"veh_123": {"pos": [10, 5], "speed": 4.0, "last_ts": 12345},"veh_B":   {"pos": [3, 4],  "speed": 2.0, "last_ts": 12346}}
    Output: ("veh_B", 5.0)

### Beacon Handling
Example: 
    Input: `/input/beacons` 
    - Format: JSON beacon sent via UDP `{"id":"veh_123","pos":[10.0,5.0],"speed":4.0,"ts":123456789}`    
    Output: /output/neighbor_summary    
    - Format: JSON line printed to stdout    
    {     
        "topic": "/v2x/neighbor_summary",    
        "count": 1,    
        "nearest": {"id":"veh_123","dist":11.18},    
        "ts": 123456999     
    }   
    

## Submission Specificaion
- You node should be written in Python
- Your node will be evaluated by an automated grading system with the commands listed.
- You are allowed to use help from outside sources but attempt without copying from generated code
- Please upload the full package in the correct folder structure to a public github repository for us to review.  



## Tips

1. You are allowed to use any resources available to you. Google is your friend!
2. (Optional but required for future) [ROS2 Humble documentation](https://docs.ros.org/en/foxy/Releases/Release-Humble-Hawksbill.html) is a great place to start if you are new to ROS. This [page](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Cpp-Publisher-And-Subscriber.html) walks you through how to create a publisher and subscriber node in c++, and this [page](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html) in python.
4. The learning curve can be steep here! We don't want you to get stuck! Feel free to send high-level questions to ejxie@wisc.edu if you have questions! Please put "[WA]" in the subject or your question may be ignored!
