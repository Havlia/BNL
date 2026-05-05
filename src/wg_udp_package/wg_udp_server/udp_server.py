import rclpy
from rclpy.node import Node
import yaml
import os
import numpy as np
import math
from sensor_msgs.msg import Image
from ament_index_python import get_package_prefix
import socket


class udp_server_node(Node):
    def __init__(self):
        super().__init__('udp_server_node')

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.hostname = socket.gethostname()
        self.ip = socket.gethostbyname(self.hostname)

        self.port = 7227

        self.server_address = ('Wall-G-Home-Computer', self.port)

        self.timer = self.create_timer(1/20, self.network_loop)

        self.get_logger().info(f"Node started")
    
    def network_loop(self):

        self.sock.bind(self.server_address)
        self.get_logger().info(f"Listening on {self.port}")

        data, server = self.sock.recvfrom(4096)
        self.get_logger().info(f"Server Reply: {data}")    

def main(args=None):
    rclpy.init(args=args)
    udp_server_N = udp_server_node()
    rclpy.spin(udp_server_N)
    udp_server_N.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()


