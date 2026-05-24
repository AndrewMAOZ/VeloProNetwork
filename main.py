# This file contains the GUI code for controlling the proxy server. It imports the core server logic from proxy_core.py and provides a simple interface to start and stop the server using buttons. The status label updates to reflect whether the server is running or stopped.
# The launch() function starts the server in a separate thread, while the halt() function signals the server to stop using the stop_server() function from proxy_core.py.
# The use of a global threading.Event in proxy_core.py allows for a clean shutdown of the server when the "Stop Proxy" button is pressed.
# Note: Ensure that proxy_core.py is in the same directory as this main.py file for the imports to work correctly.
# Reminder: remember to run proxy_core.py before running this main.py to ensure the server logic is available for the GUI to control.
# future plans: 
# - consider adding error handling in the launch() and halt() functions to manage potential issues when starting or stopping the server, such as port conflicts or server not running scenarios.
# - also consider adding a log area in the GUI to display real-time logs from the proxy server for better monitoring and debugging.
# - finally, consider implementing a more robust communication mechanism between the GUI and the server, such as using a queue or socket communication, to allow for more complex interactions and status updates beyond just starting and stopping the server.
# - get more IP adresses to access
# - add a feature to switch between different proxy servers if multiple are running
# - add a feature to configure the proxy server settings (e.g., port number, allowed IPs) from the GUI
# - add a feature to view and manage active connections through the proxy server in the GUI
# - add a feature to view logs of the proxy server in real-time within the GUI
# - add a feature to automatically restart the proxy server if it crashes or stops unexpectedly
# - add a feature to schedule automatic start and stop times for the proxy server
# - add a feature to monitor the performance of the proxy server (e.g., bandwidth usage, number of active connections) in real-time within the GUI
# - add a feature to send custom commands to the proxy server from the GUI for advanced control and configuration
# - add a feature to view and manage the configuration files of the proxy server directly from the GUI
# - add a feature to integrate with external monitoring tools or services for enhanced visibility and alerting of the proxy server's status and performance.
# - add a feature to allow remote control of the proxy server through a secure connection, enabling users to manage the server from different locations.
# - add a feature to allow users to customize the appearance of the GUI, such as changing themes or layouts, for a more personalized experience.
# - add a feature to allow users to create and manage multiple proxy server profiles with different configurations for easy switching between them.
# - add a feature to allow users to view and manage the proxy server's access control lists (ACLs) directly from the GUI for enhanced security management.
# This is not even version alpha, this is just a basic proof of concept to demonstrate the separation of concerns between the GUI and the core server logic, and to provide a simple interface for controlling the proxy server. Future iterations will focus on adding more features, improving error handling, and enhancing the overall user experience.
# version alpha will be released later with more functionality and a more polished interface, while version beta will focus on bug fixes, performance improvements, and additional features based on user feedback from the alpha release. The final version will aim to be a robust and user-friendly proxy server management tool with a wide range of features for both novice and advanced users.
# then version beta will be released with more features and improvements based on user feedback from the alpha release, and the final version will be a polished and feature-rich proxy server management tool that meets the needs of a wide range of users, from casual users to IT professionals. The development process will be iterative, with regular updates and improvements based on user feedback and testing to ensure that the final product is both functional and user-friendly.
# version 0.1 will be released after beta and will focus on usability and more ports, while version 0.2 will focus on performance optimizations and additional features such as real-time monitoring and advanced configuration options. The final version 1.0 will be a stable and feature-rich proxy server management tool that provides a seamless user experience and meets the needs of a wide range of users, from casual users to IT professionals. Regular updates and improvements will continue to be made based on user feedback and testing to ensure that the product remains relevant and useful in the ever-evolving landscape of proxy server management.
# future goals:
# - add support for multiple proxy server types (e.g., HTTP, SOCKS5) with the ability to switch between them from the GUI
# - add a feature to allow users to view and manage the proxy server's access control lists (ACLs) directly from the GUI for enhanced security management
# The ultimate goal of this project is to bypass the Great Firewall of China (GFW) and provide users with a reliable and user-friendly proxy server management tool that allows them to access blocked content and maintain their online privacy and security. By continuously improving the functionality, performance, and user experience of the tool through iterative development and user feedback, we aim to create a powerful solution that empowers users to take control of their online presence and bypass censorship effectively.
# this will be around version 4.0 or 3.0 if the development process goes smoothly and we are able to implement the necessary features and optimizations in a timely manner. The project will be an ongoing effort, with regular updates and improvements based on user feedback and testing to ensure that the final product is both functional and user-friendly, while also effectively bypassing the GFW and providing users with a reliable proxy server management tool.
# Note: The development timeline and versioning may vary based on the complexity of the features being implemented, the amount of user feedback received, and the resources available for development. Regular communication with users and stakeholders will be essential to ensure that the project stays on track and meets the needs of its target audience effectively.
# thanks for reading the notes, and enjoy the development process! Your feedback and suggestions are always welcome to help improve the project and make it a valuable tool for users looking to bypass the GFW and manage their proxy servers effectively. Stay tuned for updates and new features as we continue to develop and enhance this project!
# This is still the most basic prototype version, with more works to be done in the future to add more features, improve performance, and enhance the user experience. The current focus is on establishing a solid foundation for the proxy server management tool, with a clear separation of concerns between the GUI and the core server logic, and providing a simple interface for controlling the server. Future iterations will build upon this foundation to create a more robust and feature-rich tool that meets the needs of a wide range of users.

import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import queue
import proxy_core

# Setup
log_queue = queue.Queue()
proxy_core.set_log_queue(log_queue)

root = tk.Tk()
root.title("Proxy Alpha v0.1")
root.geometry("400x500")

# Logging Area
log_area = scrolledtext.ScrolledText(root, width=45, height=15)
log_area.pack(pady=10, padx=10, fill='both', expand=True)

# IP Selection
tk.Label(root, text="Select Bind IP:").pack()
ip_options = ["127.0.0.1 (Local Only)", "0.0.0.0 (All Interfaces)"]
selected_ip = tk.StringVar(root, value=ip_options[0])
tk.OptionMenu(root, selected_ip, *ip_options).pack(fill='x', padx=20)

# Port Selection (Combobox)
tk.Label(root, text="Select or Enter Proxy Port:").pack()
port_combobox = ttk.Combobox(root, values=["8080", "8888", "9999", "1080"])
port_combobox.current(0)
port_combobox.pack(fill='x', padx=20)

def launch():
    port_input = port_combobox.get().strip()
    try:
        port = int(port_input)
        if not (1024 <= port <= 65535):
            raise ValueError
        
        mode = selected_ip.get()
        bind_ip = "127.0.0.1" if "127.0.0.1" in mode else "0.0.0.0"
        
        threading.Thread(target=proxy_core.start_server, args=(bind_ip, port), daemon=True).start()
    except ValueError:
        log_queue.put("Error: Please select or enter a valid port (1024-65535).")

# Buttons
tk.Button(root, text="Start Proxy", command=launch, bg="#d1e7dd").pack(pady=5, padx=20, fill='x')
tk.Button(root, text="Stop Proxy", command=proxy_core.stop_server, bg="#f8d7da").pack(pady=5, padx=20, fill='x')

def check_log_queue():
    try:
        while True:
            msg = log_queue.get_nowait()
            log_area.insert(tk.END, msg + "\n")
            log_area.see(tk.END)
    except queue.Empty:
        pass
    root.after(100, check_log_queue)

check_log_queue()
root.mainloop()