import rclpy
from rclpy.node import Node
import yaml
import os
import numpy as np
import math
from sensor_msgs.msg import Image, Imu
from geometry_msgs.msg import Twist, Accel, Quaternion, Vector3
from ament_index_python import get_package_prefix
from data_utilities.qos_profiles import default_qos_profile
from RPi import GPIO
import time
import board
import busio
import adafruit_bno08x
from adafruit_bno08x.i2c import BNO08X_I2C


class imu_node_class(Node):
    def __init__(self):
        super().__init__('node_name')
        


        self.i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)
        self.bno = BNO08X_I2C(self.i2c)

        self.bno.enable_feature(adafruit_bno08x.BNO_REPORT_ROTATION_VECTOR)
        self.bno.enable_feature(adafruit_bno08x.BNO_REPORT_ACCELEROMETER)
        self.bno.enable_feature(adafruit_bno08x.BNO_REPORT_GYROSCOPE)

        self.prev_msg = None

        self.imu_pub = self.create_publisher(Imu,'imu_data', default_qos_profile) 
        self.create_timer(1/40, self.imu_callback)

        self.get_logger().info(f"Node started")
    
    def imu_callback(self):
        try:
            imu_msg         = Imu()
            quat_msg        = Quaternion()
            accel_msg       = Vector3()
            gyro_msg        = Vector3()

            quat_i, quat_j, quat_k, quat_w = self.bno.quaternion
            accel_x, accel_y, accel_z = self.bno.acceleration
            gyro_x, gyro_y, gyro_z = self.bno.gyro

            quat_msg.i = quat_i
            quat_msg.j = quat_j
            quat_msg.k = quat_k
            quat_msg.w = quat_w

            accel_msg.x = accel_x
            accel_msg.y = accel_y
            accel_msg.z = accel_z       #   evt sett herren te 0

            gyro_msg.x = gyro_x         #   evt x og y her og
            gyro_msg.y = gyro_y         #
            gyro_msg.z = gyro_z

            imu_msg.linear_acceleration = accel_msg
            imu_msg.angular_velocity    = gyro_msg
            imu_msg.orientation         = quat_msg

            if imu_msg == self.prev_msg:
                return
            
            else:
                self.imu_pub.publish(imu_msg)
                self.prev_msg = imu_msg

        except:
            self.get_logger().info("Sensor fucked up or something")

def main(args=None):
    rclpy.init(args=args)
    imu_N = imu_node_class()
    rclpy.spin(imu_N)
    imu_N.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()


