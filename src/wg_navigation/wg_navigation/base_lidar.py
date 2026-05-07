import rclpy
from rclpy.node import Node
import yaml
import os
import numpy as np
import math
from sensor_msgs.msg import Image
from ament_index_python import get_package_prefix


class node_class_name(Node):
    def __init__(self):
        super().__init__('node_name')
        
        self.get_logger().info(f"Node started")
        

def main(args=None):
    rclpy.init(args=args)
    node_name_N = node_class_name()
    rclpy.spin(node_name_N)
    node_name_N.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()


