import rclpy
from rclpy.utilities import remove_ros_args
from rclpy.node import Node
import yaml
import os
import numpy as np
import math
from sensor_msgs.msg import Image
from ament_index_python import get_package_prefix, get_package_share_directory
from PyQt5.QtGui import QIcon
from PyQt5.QtSvg import QGraphicsSvgItem
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QVBoxLayout, QFormLayout, QHBoxLayout, QPushButton, QLabel, QSpacerItem, QSizePolicy, QLCDNumber, QLineEdit, QTabWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QDoubleValidator
import sys
import cv2

class controller_gui_node(Node):
    def __init__(self):
        super().__init__('controller_gui_node')

        self.timer = QTimer()

        self.get_logger().info(f"Node started")
    
    def start_gui(self, parent=None):

        self.main_window = QWidget(parent)
        self.main_window.setWindowTitle("Wall-G Controller")

        logo_path = os.path.join(get_package_share_directory('wg_controller_gui'), 'bnl_logo.png')

        logo = QIcon(logo_path)
        self.main_window.setWindowIcon(logo)

        self.main_layout = QGridLayout(self.main_window)
        #self.main_layout.rowCount()


        self.controller_window = QWidget()
        self.controller_window.setWindowTitle("Rviz2 Window")

        self.rviz_window = QWidget()
        self.rviz_window.setWindowTitle("Rviz2 Window")
        self.rviz_render = QRe

        self.image_window = QWidget()
        self.image_window.setWindowTitle("Image Segmentation History")


        self.window_tab     = QTabWidget(parent)
        
        self.window_tab.addTab(self.controller_window, "Controller")
        self.window_tab.addTab(self.rviz_window, "Rviz2")
        self.window_tab.addTab(self.image_window, "Image History")
        
        
        
        
        self.main_layout.addWidget(self.window_tab)

        self.main_window.show()

    def on_shutdown(self):
        self.get_logger().warning("GUI exited, exiting ROS2...")

        try:
            self.timer.stop()

        except:
            self.get_logger().info("No timer attribute, moving on..")
        
        finally:
            self.destroy_node()


def main(args=None):
    
    rclpy.init(args=args)

    gui = controller_gui_node()

    # “Graceful degradation”: forsøk å starte GUI, men tåle headless miljø
    try:

        qt_args = remove_ros_args(sys.argv)
        app = QApplication(qt_args)
        app.aboutToQuit.connect(gui.on_shutdown)
        gui.start_gui()  # bygger og viser vinduet
        gui.get_logger().info("Skal ha åpnet seg")
   
    except Exception as e:
        gui.get_logger().error(f"Kunne ikke starte GUI: {e}. Kjører headless (ROS2 aktiv).")
        app = None

# ROS via Qt-timer hvis vi har GUI; ellers kjør en enkel rclpy-løkke
    if app is not None:

        gui.timer.timeout.connect(lambda: rclpy.spin_once(gui, timeout_sec=0.1))
        gui.timer.start(100)

        # Snill SIGINT-håndtering (Ctrl+C lukker Qt og ROS)
        import signal
        def signal_handler(sig, frame):
            print("SIGINT received, shutting down...")
            try:
                gui.destroy_node()
                rclpy.shutdown()
            finally:
                app.quit()
        signal.signal(signal.SIGINT, signal_handler)

        # Kjør Qt-loop
        exit_code = app.exec_()
        

        # Ekstra sikker opprydding
        try:
            gui.destroy_node()
        finally:
            if rclpy.ok():
                rclpy.shutdown()
        sys.exit(exit_code)

    else:
        # Headless fallback: pump ROS selv (ingen Qt)
        try:
            while rclpy.ok():
                rclpy.spin_once(gui, timeout_sec=0)
        except KeyboardInterrupt:
            pass
        finally:
            gui.destroy_node()
            rclpy.shutdown()

if __name__ == "__main__":
    main()
