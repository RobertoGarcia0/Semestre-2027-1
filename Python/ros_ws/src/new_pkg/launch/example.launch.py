from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='new_pkg',
            executable='publicador',
            name='publisher_node',
            output='screen'
        ),
        Node(
            package='new_pkg',
            executable='servidor_servicio',
            name='service_server',
            output='screen'
        ),
        Node(
            package='new_pkg',
            executable='servidor_accion',
            name='action_server',
            output='screen'
        )
    ])