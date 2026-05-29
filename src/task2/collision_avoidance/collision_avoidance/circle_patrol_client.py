import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
import sys

from interfaces.action import ExecuteCircle

class CirclePatrolClient(Node):
    def __init__(self):
        super().__init__('circle_patrol_client')
        
        self.aclient = ActionClient(self, ExecuteCircle, 'execute_circle')

    def send_goal(self, radius):
        self.get_logger().info('Waiting...')
        self.aclient.wait_for_server()

        g_msg = ExecuteCircle.Goal()
        g_msg.radius = float(radius)

        self.get_logger().info(f'Move in circle with {radius}m radius.')
        
        self.goalsend = self.aclient.send_goal_async(g_msg, feedback_callback=self.feedback_callback)
        self.goalsend.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        res = future.result()
        if not res.accepted:
            self.get_logger().info('Rejected by Server')
            return

        self.get_logger().info('Starting Moving...')
        
        self.resultget = res.get_result_async()
        self.resultget.add_done_callback(self.get_result_callback)

    def feedback_callback(self, feedback_msg):
        fdbk = feedback_msg.feedback
        self.get_logger().info(f'Feedback: {fdbk.current_status} | Distance Traveled: {fdbk.distance_traveled:.2f}m')

    def get_result_callback(self, future):
        res = future.result().result
        
        if res.success:
            self.get_logger().info(f'SUCCESS: {res.final_report}')
        else:
            self.get_logger().error(f'ABORTED: {res.final_report}')
            
        rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)
    node = CirclePatrolClient()
    
    if len(sys.argv)>1:
        r=float(sys.argv[1])
    else:
        r=2

    node.send_goal(r)
    rclpy.spin(node)

if __name__ == '__main__':
    main()