import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from interfaces.action import ExecuteCircle

class CirclePatrolClient(Node):
    def __init__(self):
        super().__init__('circle_patrol_client')
        
        self.aclient_client = ActionClient(self, ExecuteCircle, 'execute_circle')

    def send_goal(self, radius):
        self.get_logger().info('Waiting...')
        self.aclient_client.wait_for_server()

        g_msg = ExecuteCircle.Goal()
        g_msg.radius = float(radius)

        self.get_logger().info(f'Move in circle with {radius}m radius.')
        
        self._send_goal_future = self.aclient_client.send_goal_async(
            g_msg, 
            feedback_callback=self.feedback_callback
        )
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Rejected by Server')
            return

        self.get_logger().info('Starting Moving...')
        
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info(f'Feedback: {feedback.current_status} | Distance Traveled: {feedback.distance_traveled:.2f}m')

    def get_result_callback(self, future):
        result = future.result().result
        
        if result.success:
            self.get_logger().info(f'SUCCESS: {result.final_report}')
        else:
            self.get_logger().error(f'ABORTED: {result.final_report}')
            
        rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)
    node = CirclePatrolClient()
    
    node.send_goal(1.5)
    
    rclpy.spin(node)

if __name__ == '__main__':
    main()