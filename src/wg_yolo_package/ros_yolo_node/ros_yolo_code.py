import rclpy
from rclpy.node import Node
import yaml
import os
import numpy as np
import math
from sensor_msgs.msg import Image
from data_utilities.qos_profiles import default_qos_profile
from ament_index_python import get_package_prefix
from ultralytics import YOLO
from ultralytics.engine.results import Results
import traceback
import cv2
import cv_bridge
import torch
import datetime as dt
from hashlib import sha256

class ros_yolo(Node):
    def __init__(self):
        super().__init__('ros_yolo_node')
        
        #self.use_cuda = torch.cuda_is_available()

        if 1==0:
            self.device = 'cuda:0'
        else:
            self.device = 'cpu'

        self.model_directory    = os.path.join(get_package_prefix('wg_yolo_package'), 'share', 'wg_yolo_package', 'segmentation_model')
        self.model_path         = os.path.join(self.model_directory, 'yolo26n.pt')

        self.image_index = 1

        self.event_buffer_time = 2        #   sekund
        self.event_buffer      = []
        self.min_conf = 0.45            #   Minimum konfidens

        self.start_yolo()

        self.create_subscription(Image, 'camera_image', self.image_callback, default_qos_profile)

        self.cv_bridge = cv_bridge.CvBridge()
        self.latest_image           = None
        self.image_id               = None
        self.current_image_id       = None
        self.processing             = False


    def start_yolo(self):

        self.model = YOLO(self.model_path)
        self.get_logger().info(f"Yolo startet.")


    def image_callback(self, msg: Image):
        self.latest_image = msg
        self.image_id = dt.datetime.now().isoformat(timespec='milliseconds')
    

    def detect_image(self):
        if self.processing or self.latest_image is None:
            return


        if self.image_id == self.current_image_id:
            return
        
        self.processing = True
        self.current_image_id = self.image_id
        
        try:

            img_cv2 = np.frombuffer(self.latest_image.data, dtype=np.uint8).reshape((self.latest_image.height, self.latest_image.width, 3))
            results = self.model.predict(source=img_cv2, 
                                        conf=self.min_conf,
                                        device=self.device,
                                        classes=[46, 77],
                                        visualize=False,
                                        verbose=False
                                        )
            
            for result in results:

                if result.boxes is None or len(result.boxes) == 0:
                    return
                
                confidence = result.boxes.conf[0]

                self.get_logger().info(f"{confidence}")
                
        finally:
        
            self.processing = False

        

def main(args=None):
    rclpy.init(args=args)
    ros_yolo_N = ros_yolo()
    
    try:
        while rclpy.ok():
            rclpy.spin_once(ros_yolo_N, timeout_sec=0.01)
            ros_yolo_N.detect_image()
    
    finally:
        ros_yolo_N.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()
