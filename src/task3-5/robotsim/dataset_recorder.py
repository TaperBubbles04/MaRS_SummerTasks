#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import os

class DatasetRecorder(Node):
    def __init__(self):
        super().__init__('dataset_recorder')
        self.subscription = self.create_subscription(Image, '/camera', self.listener_callback, 10)
        self.bridge = CvBridge()
        self.count = 0
        
        self.save_path = "dataset_images"
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
            
        self.get_logger().info("--- RECORDER ACTIVE ---")

    def listener_callback(self, msg):
        if self.count % 15 == 0:
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            filename = os.path.join(self.save_path, f"rover_view_{self.count}.jpg")
            cv2.imwrite(filename, cv_image)
            self.get_logger().info(f'Saved: {filename}')
        self.count += 1

def main(args=None):
    rclpy.init(args=args)
    node = DatasetRecorder()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()