#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from ultralytics import YOLO
import os

class ConeDetector(Node):
    def __init__(self):
        super().__init__('cone_detector')
        
        self.bridge = CvBridge()
        
        self.subscription = self.create_subscription(
            Image,
            '/camera', 
            self.image_callback,
            10)
            
        current_dir = os.path.dirname(os.path.realpath(__file__))
        weights_path = os.path.join(current_dir, 'best.pt')
        
        print(f"\n[INFO] Looking for weights at: {weights_path}")
        
        if not os.path.exists(weights_path):
            print(f"[ERROR] Could not find best.pt at {weights_path}! Check file placement.")
            return

        self.model = YOLO(weights_path)
        print("[SUCCESS] YOLO model loaded! Waiting for Gazebo camera frames...\n")

    def image_callback(self, msg):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            
            results = self.model(cv_image, verbose=False)
            
            annotated_frame = results[0].plot()
            
            cv2.imshow("Mars Rover - Live Cone Detection", annotated_frame)
            cv2.waitKey(1)
        except Exception as e:
            print(f"[ERROR] Callback failed: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = ConeDetector()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("\nShutting down detection node.")
    finally:
        node.destroy_node()
        cv2.destroyAllWindows()
        rclpy.shutdown()

if __name__ == '__main__':
    main()