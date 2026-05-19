# MaRS Summer Tasks

## Task-1:

### What I Learned
* **Workspaces:** I learned how to create a ROS2 workspace (e.g., `~/ros2_ws/src`) to isolate project development.
* **Building & Sourcing:** I used  `colcon build` to compile the packages. I also learned the importance of overlaying the workspace onto the base ROS2 installation by sourcing the `install/setup.zsh` file, which allows my terminal to recognize my custom executables.
* **Package Creation:** I created a Python based package using `ament_python` and a C++ package (`cpp_pubsub`) using `ament_cmake`. I also learned that a package acts like a container which can be used as seperate modules for certain tasks.
* **Dependencies:** I learned `rosdep` to automatically check and install missing dependencies in the `package.xml`.
* **Configuration:** I configured the `setup.py` file to tell the system where my nodes' code is located so they can be executed from the CLI. I also learned how to link dependencies and compile source files into executable nodes by modifying `CMakeLists.txt` and understood how to configure the `install()` so the system knows where to find the compiled code so that it can be executed.
* **Publisher:** Wrote a `Publisher_Node` that continuously sends a string message over a specific topic (`/Channel1` and `/Channel2`).
* **Subscriber:** Wrote a `Subscriber_Node` that listens to the topic and uses a callback function to log the data it receives to the terminal.
* **Smart Pointers:** I learned how to initialize nodes and components using `std::make_shared` and `SharedPtr` to prevent memory leaks.
* **Const Usage:** I learned the importance of passing the message variables as const (`const std_msgs::msg::String &msg`) to protect data and save RAM.
* **String Version:** I also learned how to use `.c_str()` to connect current C++ strings with the logging functions (`RCLCPP_INFO`) since it is of older C-style.
---

### CLI Outputs & Visualization(Python)

I used the following ROS2 CLI tools:

*(Screenshot of the terminal running node/topic lists and topic echo)*
![Node List](images/PythonNode.png)

*(RQT Graph)*

![RQT Graph](images/Pythonrqtgraph.png)

### CLI Outputs & Visualization (C++ Nodes)

I used the following ROS2 CLI tools:

*(Screenshot of the terminal running node/topic lists and topic echo)*
![Node List](images/CPPNode.png)

*(RQT Graph)*

![RQT Graph](images/CPPRQTgraph.png)

---