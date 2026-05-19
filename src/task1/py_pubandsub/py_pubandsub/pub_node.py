import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Publisher_Node(Node):
    def __init__(self):
        super().__init__('Publisher_Node')
        self.publisher_ = self.create_publisher(String, 'Channel1', 10)
        self.timer = self.create_timer(1, self.publish_callback)
        self.i=0

    def publish_callback(self):
        msg = String()
        msg.data = f'{self.i}' 
        self.publisher_.publish(msg)
        self.get_logger().info("Publishing...")
        self.i+=1


def main(args=None):
    rclpy.init(args=args)
    pub_node = Publisher_Node()
    rclpy.spin(pub_node)
    pub_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()