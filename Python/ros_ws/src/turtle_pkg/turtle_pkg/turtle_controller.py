import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from rcl_interfaces.msg import SetParametersResult
from geometry_msgs.msg import Twist

class TurtleController(Node):
    def __init__(self):
        super().__init__('turtle_controller')

        self.declare_parameter('linear_velocity', 1.0)
        self.declare_parameter('angular_velocity', 0.0)
        self.declare_parameter('duration', 5.0)

        self.linear_velocity = self.get_parameter('linear_velocity').value
        self.angular_velocity = self.get_parameter('angular_velocity').value
        self.duration = self.get_parameter('duration').value

        self.publisher = self.create_publisher(
            Twist,
            '/turtle1/cmd_vel',
            10
        )

        self.start_time = self.get_clock().now()
        self.timer = self.create_timer(0.1, self.control_turtle)

        self.add_on_set_parameters_callback(self.parameter_callback)

    def parameter_callback(self, parameters):
        for parameter in parameters:
            if parameter.name == 'linear_velocity':
                self.linear_velocity = parameter.value
            elif parameter.name == 'angular_velocity':
                self.angular_velocity = parameter.value
            elif parameter.name == 'duration':
                self.duration = parameter.value

        return SetParametersResult(successful=True)

    def control_turtle(self):
        elapsed = (
            self.get_clock().now() - self.start_time
        ).nanoseconds / 1e9

        msg = Twist()

        if elapsed < self.duration:
            msg.linear.x = self.linear_velocity
            msg.angular.z = self.angular_velocity
        else:
            msg.linear.x = 0.0
            msg.angular.z = 0.0

        self.publisher.publish(msg)

        if elapsed >= self.duration:
            self.get_logger().info('Movimiento terminado')
            self.timer.cancel()

def main(args=None):
    rclpy.init(args=args)
    node = TurtleController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()