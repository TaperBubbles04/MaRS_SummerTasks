#!/usr/bin/env python3
import os
os.environ['QT_LOGGING_RULES'] = '*=false' 

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import cv2.aruco as aruco
import numpy as np

from geometry_msgs.msg import TransformStamped, PoseStamped
from tf2_ros import StaticTransformBroadcaster, Buffer, TransformListener
import tf2_geometry_msgs 

class ArucoDetector(Node):
    def __init__(self):
        super().__init__('aruco_detector')
        self.subscription = self.create_subscription(Image, '/camera', self.image_callback, 10)
        self.bridge = CvBridge()
        
        self.tf_static_broadcaster = StaticTransformBroadcaster(self)
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        
        self.marker_observations = {}  
        self.published_markers = set() 
        
        self.camera_matrix = np.array([
            [476.7, 0.0, 400.0],
            [0.0, 476.7, 400.0],
            [0.0, 0.0, 1.0]
        ], dtype=np.float32)
        self.dist_coeffs = np.zeros((5, 1), dtype=np.float32)
        
        self.get_logger().info("Visual Cortex Online: Scanning for ArUco Markers...")

    def image_callback(self, msg):
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        
        dictionary = aruco.getPredefinedDictionary(aruco.DICT_5X5_250)
        parameters = aruco.DetectorParameters()
        detector = aruco.ArucoDetector(dictionary, parameters)
        corners, ids, rejected = detector.detectMarkers(gray)

        if ids is not None:
            aruco.drawDetectedMarkers(cv_image, corners, ids)
            
            marker_size = 0.2 
            rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(corners, marker_size, self.camera_matrix, self.dist_coeffs)
            
            for i in range(len(ids)):
                marker_id = ids[i][0]
                
                cv2.putText(cv_image, f"ID: {marker_id}", 
                            (int(corners[i][0][0][0]), int(corners[i][0][0][1]) - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                if marker_id in self.published_markers:
                    continue 
                
                self.marker_observations[marker_id] = self.marker_observations.get(marker_id, 0) + 1
                
                if self.marker_observations[marker_id] >= 5:
                    try:
                        trans = self.tf_buffer.lookup_transform('odom', 'camera_link', rclpy.time.Time())
                        
                        p_cam = PoseStamped()
                        p_cam.header.frame_id = 'camera_link'
                        p_cam.pose.position.x = float(tvecs[i][0][0])
                        p_cam.pose.position.y = float(tvecs[i][0][1])
                        p_cam.pose.position.z = float(tvecs[i][0][2])
                        p_cam.pose.orientation.w = 1.0 
                        
                        # Calculate Global Location
                        p_global_pose = tf2_geometry_msgs.do_transform_pose(p_cam.pose, trans)
                        
                        # --- EXPLICIT GLOBAL POSITION TERMINAL READOUT ---
                        gx = p_global_pose.position.x
                        gy = p_global_pose.position.y
                        gz = p_global_pose.position.z
                        
                        self.get_logger().info(f"")
                        self.get_logger().info(f"Marker ID: {marker_id}")
                        self.get_logger().info(f"Coordinates -> X: {gx:.3f}m | Y: {gy:.3f}m | Z: {gz:.3f}m")
                        # -------------------------------------------------

                        t = TransformStamped()
                        t.header.stamp = self.get_clock().now().to_msg()
                        t.header.frame_id = 'odom'
                        t.child_frame_id = f'global_aruco_{marker_id}'
                        
                        t.transform.translation.x = gx
                        t.transform.translation.y = gy
                        t.transform.translation.z = gz
                        t.transform.rotation = p_global_pose.orientation
                        
                        self.tf_static_broadcaster.sendTransform(t)
                        self.published_markers.add(marker_id)
                        
                    except Exception as e:
                        self.get_logger().warn(f"TF Error for ID {marker_id}: {e}")

        cv2.imshow("Rover Camera View", cv_image)
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    node = ArucoDetector()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()