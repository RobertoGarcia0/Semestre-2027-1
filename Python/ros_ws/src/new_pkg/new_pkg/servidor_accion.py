import asyncio
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse, CancelResponse
from example_interfaces.action import Fibonacci

class FibonacciActionServer(Node):
    def __init__(self):
        super().__init__('fibonacci_action_server')
        self.action_server = ActionServer(
            self,
            Fibonacci,
            '/fibonacci',
            execute_callback=self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback
        )

    def goal_callback(self, goal_request):
        self.get_logger().info(
            f'Objetivo recibido: orden {goal_request.order}'
        )
        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle):
        self.get_logger().info('Solicitud de cancelación recibida')
        return CancelResponse.ACCEPT

    async def execute_callback(self, goal_handle):
        order = goal_handle.request.order
        feedback = Fibonacci.Feedback()
        result = Fibonacci.Result()

        sequence = [0, 1]

        for i in range(2, order):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                result.sequence = sequence
                return result

            sequence.append(sequence[i - 1] + sequence[i - 2])

            feedback.sequence = sequence
            goal_handle.publish_feedback(feedback)

            self.get_logger().info(f'Progreso: {sequence}')


        goal_handle.succeed()
        result.sequence = sequence[:order]

        self.get_logger().info(f'Resultado: {result.sequence}')

        return result

def main(args=None):
    rclpy.init(args=args)
    node = FibonacciActionServer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()