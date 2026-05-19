import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Subscriber_Node(Node):
    def __init__(self):
        super().__init__('Subscriber_Node')
        self.subscription = self.create_subscription(String, 'Channel1', self.listen_callback, 10)
        self.subscription

    def listen_callback(self, msg):
        self.get_logger().info(f'Seconds Elapsed:{msg.data}')

def main(args=None):
    rclpy.init(args=args)
    sub_node=Subscriber_Node()
    rclpy.spin(sub_node)
    sub_node.destory_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()