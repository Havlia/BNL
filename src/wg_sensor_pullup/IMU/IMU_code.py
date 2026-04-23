import rclpy
from rclpy.node import Node
import yaml
import os
import numpy as np
import math
from sensor_msgs.msg import Image
from ament_index_python import get_package_prefix
from RPi import GPIO


class imu_node_class(Node):
    def __init__(self):
        super().__init__('node_name')
        
        self.get_logger().info(f"Node started")
        

def main(args=None):
    rclpy.init(args=args)
    imu_N = imu_node_class()
    rclpy.spin(imu_N)
    imu_N.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()


