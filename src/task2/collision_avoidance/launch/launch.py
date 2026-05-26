from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='sim'
        ),
        
        Node(
            package='collision_avoidance',
            executable='collision_avoidance_node',
            name='collision_avoidance_node',
            parameters=[
                {'sfty_thd': 2.0} 
            ]
        )
    ])