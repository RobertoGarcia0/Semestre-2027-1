import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from example_interfaces.action import Fibonacci
from rclpy.task import Future
from rclpy.action.client import ClientGoalHandle

class FibonacciActionClient(Node):
    def __init__(self):
        super().__init__('fibonacci_action_client')
        self.action_client = ActionClient(
            self,
            Fibonacci,
            '/fibonacci'
        )

    def feedback_callback(self, feedback_msg:Fibonacci.Impl.FeedbackMessage):
        self.get_logger().info(
            f'Feedback: {feedback_msg.feedback.sequence}'
        )

    def send_goal(self, order):
        self.action_client.wait_for_server()

        goal = Fibonacci.Goal()
        goal.order = order

        future:Future = self.action_client.send_goal_async(
            goal,
            feedback_callback=self.feedback_callback
        )

        rclpy.spin_until_future_complete(self, future)

        goal_handle:ClientGoalHandle = future.result()

        if not goal_handle.accepted:
            self.get_logger().info('Objetivo rechazado')
            return

        self.get_logger().info('Objetivo aceptado')

        result_future:Future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(self, result_future)

        result:Fibonacci.Result = result_future.result().result
        
        self.get_logger().info(
            f'Resultado final: {result.sequence}'
        )

def main(args=None):
    rclpy.init(args=args)
    node = FibonacciActionClient()

    node.send_goal(10)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()