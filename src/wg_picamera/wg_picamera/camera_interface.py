import rclpy
from rclpy.node import Node
import yaml
import os
import numpy as np
import math
from sensor_msgs.msg import Image
from data_utilities.qos_profiles import default_qos_profile
from ament_index_python import get_package_prefix
import cv2
import datetime as dt
from hashlib import sha256
from time import sleep
import subprocess as sp
import threading
import gc


class ros_picamera(Node):
    def __init__(self):
        super().__init__('picamera_node')

        self.image_publisher = self.create_publisher(Image, 'camera_image', default_qos_profile)
        self.timer = self.create_timer(1/5, self.image_callback)

        self.width = 640
        self.height = 480

        self.sub_command = ['sudo', 'rpicam-vid',
                            '-t', '0',
                            '--framerate','10',
                            #'--nopreview',
                            f'--width={self.width}', f'--height={self.height}',
                            '--codec', 'mjpeg',
                            '-o', '-', 
                           ]

        self.proc = sp.Popen(self.sub_command, stdout=sp.PIPE, bufsize=0)
        self.buf = b""

        self.latest_frame = None
        self.lock = threading.Lock()

        self.get_logger().info("Fakk u")

        self.thread = threading.Thread(target=self.camera_loop, daemon=True)
        self.thread.start()

    def camera_loop(self):
        while rclpy.ok():
            gc.collect()
            self.buf += self.proc.stdout.read(65536)

            if len(self.buf) > 1_000_000:
                self.buf = self.buf[-500_000:]

            #   jpg sjit
            start = self.buf.find(b'\xff\xd8')
            end =   self.buf.find(b'\xff\xd9')

            if start != -1 and end != -1 and end > start:

                jpg = self.buf[start:end+2]
                self.buf = self.buf[end+2:]

                img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                img = cv2.rotate(img, cv2.ROTATE_180)

                if img is not None:
                    pass

            else:
                img = None

            with self.lock:
                if img is not None:
                    self.latest_frame = img

    
    def image_callback(self):
        with self.lock:
            frame = self.latest_frame
        

        if frame is None:
            return

        image_msg = Image()

        image_msg.height = self.height
        image_msg.width = self.width
        image_msg.encoding = "bgr8"
        image_msg.step = self.width * 3
        image_msg.data = frame.tobytes()

        self.image_publisher.publish(image_msg)

def main(args=None):
    rclpy.init(args=args)
    picamera_N = ros_picamera()
    rclpy.spin(picamera_N)
    picamera_N.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()

