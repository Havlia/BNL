import rclpy
from rclpy.node import Node
import yaml
import os
import numpy as np
import math
from sensor_msgs.msg import Image
from data_utilities.qos_profiles import default_qos_profile
from ament_index_python import get_package_prefix
from 
import cv2
import datetime as dt
from hashlib import sha256

class ros_picamera(Node):
    def __init__(self):
        super().__init__('picamera_node')
        
        self.get_logger().info(f"Kamera starta.")

        self.picamera = Picamera2()

        

def main(args=None):
    rclpy.init(args=args)
    picamera_N = ros_picamera()
    rclpy.spin(picamera_N)
    picamera_N.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()

