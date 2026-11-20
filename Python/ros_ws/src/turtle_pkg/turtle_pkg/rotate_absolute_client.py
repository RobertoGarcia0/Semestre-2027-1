import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from turtlesim.action import RotateAbsolute

class RotateAbsoluteClient(Node):
    def __init__(self):
        super().__init__('rotate_absolute_client')
        self.action_client = ActionClient(
            self,
            RotateAbsolute,
            '/turtle1/rotate_absolute'
        )

    def feedback_callback(self, feedback_msg):
        self.get_logger().info(
            f'Ángulo restante: {feedback_msg.feedback.remaining:.3f} rad'
        )

    def send_goal(self, theta):
        self.action_client.wait_for_server()

        goal = RotateAbsolute.Goal()
        goal.theta = theta

        future = self.action_client.send_goal_async(
            goal,
            feedback_callback=self.feedback_callback
        )

        rclpy.spin_until_future_complete(self, future)

        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().info('Objetivo rechazado')
            return

        self.get_logger().info('Objetivo aceptado')

        result_future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(self, result_future)

        result = result_future.result().result

        self.get_logger().info(
            f'Rotación completada. Desplazamiento: {result.delta:.3f} rad'
        )

def main(args=None):
    rclpy.init(args=args)
    node = RotateAbsoluteClient()

    node.send_goal(1.57)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()