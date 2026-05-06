import rclpy
from rclpy.node import Node
import numpy as np
from data_utilities.qos_profiles import default_qos_profile
from ament_index_python import get_package_prefix
import board
import busio
import digitalio

class pwm_test(Node):
    def __init__(self):
        super().__init__('pwm_test_Node')

        pin = digitalio.DigitalInOut(board.D4)
        i2c = busio-I2C(board.SCL, board.SDA)

        self.get_logger().info("Woop woop")

def main(args=None):
    rclpy.init(args=args)
    pwm_test_N = pwm_test()
    rclpy.spin(pwm_test_N)
    pwm_test_N.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()

