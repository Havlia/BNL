import rclpy
from rclpy.node import Node
import yaml
import os
import numpy as np
import math
from data_utilities.qos_profiles import default_qos_profile
from sensor_msgs.msg import Image
from wg_interface.msg import ControlEvent
from ament_index_python import get_package_prefix
from RPi import GPIO
import data_utilities.headers as headers 

class control_node(Node):
    def __init__(self):
        super().__init__('control_node')
        
        self.get_logger().info(f"Node started")

        self.pwm_base_frequency = 20000

        self.pwm_pin_r = 12
        self.pwm_pin_l = 13

        self.direction_pin_r = 16
        self.direction_pin_l = 6

        self.pwm_r = GPIO.PWM(self.pwm_pin_r, self.pwm_base_frequency)
        self.pwm_l = GPIO.PWM(self.pwm_pin_l, self.pwm_base_frequency)

        self.pwm_r.start(0)
        self.pwm_l.start(0)

        self.right_direction = None
        self.left_direction = None

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pwm_pin_r, GPIO.OUT)
        GPIO.setup(self.pwm_pin_l, GPIO.OUT)

        GPIO.setup(self.direction_pin_r, GPIO.OUT)
        GPIO.setup(self.direction_pin_l, GPIO.OUT)

        self.create_subscription(ControlEvent, 'control_event_topic', self.control_event_callback, default_qos_profile)


    def control_event_callback(self, msg: ControlEvent):

        if not msg.combined_cycle or not msg.left_cycle or not msg.right_cycle:
            raise Exception(f"Syklus er ikke definert. Stopper node.")

        if msg.control_type == headers.BOTH or msg.control_type == headers.INVERSE:
            
            if msg.combined_cycle > 100:
                raise Exception(f"Duty syklus er større enn 100. Dette er ikke tilatt:  c -> float64 [0,1].")

            combined_cycle = msg.combined_cycle
            self.get_spin_direction(msg)

            GPIO.output(self.pwm_pin_r, self.right_direction)
            GPIO.output(self.pwm_pin_l, self.left_direction)

            GPIO.PWM.ChangeDutyCycle(self.pwm_pin_r, combined_cycle)
            GPIO.PWM.ChangeDutyCycle(self.pwm_pin_l, combined_cycle)
        
        elif msg.control_type == headers.RIGHT or msg.control_type == headers.LEFT:
            
            if msg.right_cycle > 100 or msg.left_cycle > 100:
                raise Exception(f"Duty syklus er større enn 100. Dette er ikke tilatt:  c -> float64 [0,1].")

            right_cycle = msg.right_cycle
            left_cycle  = msg.left_cycle

            self.pwm_r.ChangeDutyCycle(self.pwm_pin_r, right_cycle)
            self.pwm_l.ChangeDutyCycle(self.pwm_pin_l, left_cycle)
        
        else:
            raise Exception(f"Ugyldig kontroll type: n -> uint8[0,3].  Bruk c_modes.STATE for å velge kontroll type.")

    def get_spin_direction(self, mes: ControlEvent):    #   ikke en callback
    
        if not mes.combined_rotation and not mes.combined_direction:
            self.get_logger().warn(f"Mangler retningsinput, bruker forover...")
            
            self.right_direction    = headers.FORWARD
            self.left_direction     = headers.FORWARD

        if mes.control_type == headers.INVERSE:
            
            if mes.combined_rotation == headers.CLKWISE:

                self.right_direction = headers.BACKWARD 
                self.left_direction = headers.FORWARD
            
            elif mes.combined_rotation == headers.COUNTCLKWISE:
                self.right_direction = headers.FORWARD 
                self.left_direction = headers.BACKWARD
            
            else:
                raise Exception(f"Ugyldig verdi for rotasjonsretning: d -> uint8 [0, 1]")

def main(args=None):
    rclpy.init(args=args)
    control_N = control_node()
    rclpy.spin(control_N)
    control_N.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()


