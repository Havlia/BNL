import rclpy
from rclpy.node import Node
import yaml
import os
import numpy as np
import math
from sensor_msgs.msg import Image
from utilities.qos_profiles import default_qos_profile
from yolact_submodule.yolact import Yolact as yola
from ament_index_python import get_package_prefix


import traceback

class ros_yolact(Node):
    def __init__(self):
        super().__init__('ros_yolact_node')

        self.create_subscription(Image, 'camera_image', self.image_callback, default_qos_profile)


        self.get_logger().info("Node started. Venv is good")    

    def image_callback(self, msg: Image):
        self.get_logger().info(f"{get_package_prefix('yolact_venv')}")
        #self.get_logger().info(f"{msg.data}")

def main(args=None):
    rclpy.init(args=args)
    ros_yolact_N = ros_yolact()
    rclpy.spin(ros_yolact_N)
    ros_yolact_N.destroy_node()
    rclpy.shutdown()
