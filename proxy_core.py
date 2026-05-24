# This file contains the core proxy server logic, separated from the GUI code in main.py.
# It uses a global threading.Event to signal the server to stop, allowing for a clean shutdown
# when the "Stop Proxy" button is pressed in the GUI. The start_server() function listens for incoming connections and handles them, while the stop_server() function sets the event to signal the server to stop accepting new connections and shut down gracefully.
# Note: Ensure that this file is in the same directory as main.py for the imports to work correctly, and remember to run this file before running main.py to ensure the server logic is available for the GUI to control.
# future plans:
# - consider adding error handling in the start_server() function to manage potential issues such as port
#   conflicts or network errors, and to provide feedback to the GUI for better user experience.
# - also consider adding logging functionality to the server to track incoming connections, errors, and other events for better monitoring and debugging.
# - finally, consider implementing a more robust communication mechanism between the GUI and the server, such as using a queue or socket communication, to allow for more complex interactions and status updates beyond just starting and stopping the server.
# - add support for multiple proxy server types (e.g., HTTP, SOCKS5) with the ability to switch between them from the GUI
# - add a feature to allow users to view and manage the proxy server's access control lists
#   (ACLs) directly from the GUI for enhanced security management
# The ultimate goal of this project is to bypass the Great Firewall of China (GFW) and provide users with a reliable and user-friendly proxy server management tool that allows them to access blocked content and maintain their online privacy and security. By continuously improving the functionality, performance, and user experience of the tool through iterative development and user feedback, we aim to create a powerful solution that empowers users to take control of their online presence and bypass censorship effectively.
# this will be around version 4.0 or 3.0 if the development process goes smoothly and we are able to implement the necessary features and optimizations in a timely manner. The project will be an ongoing effort, with regular updates and improvements based on user feedback and testing to ensure that the final product is both functional and user-friendly, while also effectively bypassing the GFW and providing users with a reliable proxy server management tool.
# Note: The development timeline and versioning may vary based on the complexity of the features being
# for this program, the future is to get more IP addresses to access, add a feature to switch between different proxy servers if multiple are running, add a feature to configure the proxy server settings (e.g., port number, allowed IPs) from the GUI, add a feature to view and manage active connections through the proxy server in the GUI, add a feature to view logs of the proxy server in real-time within the GUI, add a feature to automatically restart the proxy server if it crashes or stops unexpectedly, add a feature to schedule automatic start and stop times for the proxy server, add a feature to monitor the performance of the proxy server (e.g., bandwidth usage, number of active connections) in real-time within the GUI, add a feature to send custom commands to the proxy server from the GUI for advanced control and configuration, add a feature to view and manage the configuration files of the proxy server directly from the GUI, add a feature to integrate with external monitoring tools or services for enhanced visibility and alerting of the proxy server's status and performance, add a feature to allow remote control of the proxy server through a secure connection, enabling users to manage the server from different locations, add a feature to allow users to customize the appearance of the GUI, such as changing themes or layouts, for a more personalized experience, add a feature to allow users to create and manage multiple proxy server profiles with different configurations for easy switching between them, add a feature to allow users to view and manage the proxy server's access control lists (ACLs) directly from the GUI for enhanced security management. The ultimate goal of this project is to bypass the Great Firewall of China (GFW) and provide users with a reliable and user-friendly proxy server management tool that allows them to access blocked content and maintain their online privacy and security. By continuously improving the functionality, performance, and user experience of the tool through iterative development and user feedback, we aim to create a powerful solution that empowers users to take control of their online presence and bypass censorship effectively. This is still the most basic prototype version, with more works to be done in the future to add more features, improve performance, and enhance the user experience. The current focus is on establishing a solid foundation for the proxy server management tool, with a clear separation of concerns between the GUI and the core server logic, and providing a simple interface for controlling the server. Future iterations will build upon this foundation to create a more robust and feature-rich tool that meets the needs of a wide range of users.
# and also able to access blobked contents such as jioHotstar, Netflix, etc. in China. The development timeline and versioning may vary based on the complexity of the features being implemented, the amount of user feedback received, and the resources available for development. Regular communication with users and stakeholders will be essential to ensure that the project stays on track and meets the needs of its target audience effectively. Thanks for reading the notes, and enjoy the development process! Your feedback and suggestions are always welcome to help improve the project and make it a valuable tool for users looking to bypass the GFW and manage their proxy servers effectively. Stay tuned for updates and new features as we continue to develop and enhance this project! This is still the most basic prototype version, with more works to be done in the future to add more features, improve performance, and enhance the user experience. The current focus is on establishing a solid foundation for the proxy server management tool, with a clear separation of concerns between the GUI and the core server logic, and providing a simple interface for controlling the server. Future iterations will build upon this foundation to create a more robust and feature-rich tool that meets the needs of a wide range of users.

import socket
import threading

log_queue = None
stop_event = threading.Event()

def set_log_queue(q):
    global log_queue
    log_queue = q

def log(message):
    if log_queue:
        log_queue.put(message)

def start_server(bind_ip, port):
    stop_event.clear()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server.bind((bind_ip, port))
        server.listen(5)
        server.settimeout(1.0)
        log(f"Proxy active on {bind_ip}:{port}")
        
        while not stop_event.is_set():
            try:
                client, addr = server.accept()
                log(f"Connection from {addr[0]}")
                client.close() 
            except socket.timeout:
                continue
    except Exception as e:
        log(f"Critical error: {e}")
    finally:
        server.close()
        log("Proxy server stopped.")

def stop_server():
    stop_event.set()