import rclpy
from rclpy.node import Node
import yaml
import os
import numpy as np
import math
from sensor_msgs.msg import Image, LaserScan
from nodes.qos_profiles import default_qos_profile

import traceback

class print_stats(Node):
    def __init__(self):
        super().__init__('test_node')
        self.create_subscription(Image, 'camera',self.camera_callback, default_qos_profile)
        self.create_subscription(LaserScan, 'scan_gpu',self.lidar_callback, default_qos_profile)
        
    def camera_callback(self, msg: Image):

        #print(f"{msg.data}")
        pass

    def lidar_callback(self, msg: LaserScan):

        print(f"{msg.ranges}")
        pass

def main(args=None):
    rclpy.init(args=args)
    ps_N = print_stats()
    rclpy.spin(ps_N)
    ps_N.destroy_node()
    rclpy.shutdown()