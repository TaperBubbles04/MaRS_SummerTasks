import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

from rclpy.qos import qos_profile_sensor_data

class CollisionAvoidanceNode(Node):
    def __init__(self):
        super().__init__('collision_avoidance_node')

        self.declare_parameter('sfty_thd', 1.5)

        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        self.sub = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            qos_profile_sensor_data
        )

    def pose_callback(self, msg: Pose):
        thd = self.get_parameter('sfty_thd').value
        x = msg.x
        y = msg.y
        cmd = Twist()

        if x < thd or x > (11.0 - thd) or y < thd or y > (11.0 - thd):
            cmd.linear.x = 1.0
            cmd.angular.z = 2.0 
            self.get_logger().info(f'Detected Wall. Rerouting... (Threshold: {thd})')
        else:
            cmd.linear.x = 2.0
            cmd.angular.z = 0.0

        self.pub.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    node = CollisionAvoidanceNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()