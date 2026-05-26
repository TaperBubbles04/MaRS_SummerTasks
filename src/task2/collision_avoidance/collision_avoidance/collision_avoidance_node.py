import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

from rclpy.qos import qos_profile_sensor_data

class CollisionAvoidanceNode(Node):
    def __init__(self):
        super().__init__('collision_avoidance_node')

        self.declare_parameter('safety_threshold', 1.5)

        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        self.subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            qos_profile_sensor_data
        )

    def pose_callback(self, msg: Pose):
        threshold = self.get_parameter('safety_threshold').value
        x = msg.x
        y = msg.y
        cmd = Twist()

        if x < threshold or x > (11.0 - threshold) or y < threshold or y > (11.0 - threshold):
            cmd.linear.x = 0.5
            cmd.angular.z = 1.5 
            self.get_logger().info(f'Wall detected! Spinning away. (Threshold: {threshold})')
        else:
            cmd.linear.x = 1.5
            cmd.angular.z = 0.0

        self.publisher_.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    node = CollisionAvoidanceNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()