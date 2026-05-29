import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

from interfaces.action import ExecuteCircle
from rclpy.action import ActionServer

from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup
import math
import time

class CirclePatrolServer(Node):
    def __init__(self):
        super().__init__('circle_patrol_server')
        
        cbg = ReentrantCallbackGroup()
        
        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.sub = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10, callback_group=cbg)
        
        self._action_server = ActionServer(self, ExecuteCircle, 'execute_circle', self.execute_callback, callback_group=cbg)
        
        self.curpos = None
        self.declare_parameter('thd', 1.0)
        self.get_logger().info('Waiting for radius coordinates...')

    def pose_callback(self, msg: Pose):
        self.curpos = msg

    def execute_callback(self, turt):
        radius = turt.request.radius
        self.get_logger().info(f'Moving in circle with {radius}m radius.')
        
        while self.curpos is None:
            time.sleep(0.1)
            
        sx = self.curpos.x
        sy = self.curpos.y
        lx = sx
        ly = sy
        
        v = 1.5 
        w = v / radius 
        
        cmd = Twist()
        cmd.linear.x = v
        cmd.angular.z = w
        
        thd = self.get_parameter("thd").value
        dist = 0.0
        circ = 2 * math.pi * radius
        
        fmsg = ExecuteCircle.Feedback()
        result = ExecuteCircle.Result()

        while rclpy.ok():
            if not turt.is_active:
                return ExecuteCircle.Result()

            x = self.curpos.x
            y = self.curpos.y
             
            if x < thd or x > (11.0 - thd) or y < thd or y > (11.0 - thd):
                cmd.linear.x = 0.0
                cmd.angular.z = 0.0
                self.pub.publish(cmd) 
                
                turt.abort() 
                result.success = False
                result.final_report = "Mission Aborted: Boundary Collision Imminent!"
                self.get_logger().error(result.final_report)
                return result

            step = math.sqrt((x - lx)**2 + (y - ly)**2)
            dist += step
            lx = x
            ly = y
            
            fmsg.distance_traveled = dist
            fmsg.current_status = "Moving..."
            turt.publish_feedback(fmsg)
            
            disp = math.sqrt((x - sx)**2 + (y - sy)**2)
            
            if dist > (circ* 0.5) and disp < 0.2:
                cmd.linear.x = 0.0
                cmd.angular.z = 0.0
                self.pub.publish(cmd)
                
                turt.succeed()
                result.success = True
                result.final_report = "Full loop completed"
                self.get_logger().info(result.final_report)
                return result
            
            if dist > (circ * 1.5):
                cmd.linear.x = 0.0
                cmd.angular.z = 0.0
                self.pub.publish(cmd)
                
                turt.abort()
                result.success = False
                result.final_report = "Mission Aborted: Failed to locate start point."
                return result

            self.pub.publish(cmd)
            time.sleep(0.05)


def main(args=None):
    rclpy.init(args=args)
    node = CirclePatrolServer()
    executor = MultiThreadedExecutor()
    rclpy.spin(node, executor=executor)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()