import rclpy
from rclpy.node import Node
import yaml
import os
import numpy as np
import math
from sensor_msgs.msg import Image
from ament_index_python import get_package_prefix
import gpiozero as gpz
import board
import busio
import adafruit_pca9685


class motor_encoder(Node):
    def __init__(self):
        super().__init__('encoder_node')
        
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.pca = adafruit_pca9685.PCA9685(self.i2c)

        self.left_channel_A = gpz.InputDevice(5)
        self.left_channel_B = gpz.InputDevice(6)

        self.right_channel_A = gpz.InputDevice(13)
        self.right_channel_B = gpz.InputDevice(26)

        self.tick_count = 0
        self.prev_tick_count = 0

        self.encoder_publish = self.create_publisher()

        self.create_timer(1/1000, self.read_output)

        # Create a simple PCA9685 class instance.
        self.pca = adafruit_pca9685.PCA9685(self.i2c)

        # Set the PWM frequency to 60hz.
        self.pca.frequency = 200

        self.get_logger().info(f"Node started")

        self.drive()


    def drive(self):
        self.pca.channels[0].duty_cycle = 0xFFFF
        self.pca.channels[1].duty_cycle = 0xFFFF

    def read_output(self):
        self.get_logger(self.left_channel_A())
        self.get_logger(self.right_channel_A())

    def close_gpio(self):
        self.left_channel_A.close()
        self.left_channel_B.close()
        self.right_channel_A.close()
        self.right_channel_B.close()

def main(args=None):
    rclpy.init(args=args)
    encoder_N = motor_encoder()
    rclpy.spin(encoder_N)
    encoder_N.close_gpio()
    encoder_N.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()


