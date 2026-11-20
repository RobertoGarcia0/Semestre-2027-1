import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class ServiceClient(Node):
    def __init__(self):
        super().__init__('service_client')
        self.client = self.create_client(AddTwoInts, '/sumar')

    def send_request(self, a, b):
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Esperando al servidor...')

        request = AddTwoInts.Request()
        request.a = a
        request.b = b

        future = self.client.call_async(request)
        rclpy.spin_until_future_complete(self, future)

        return future.result()

def main(args=None):
    rclpy.init(args=args)
    node = ServiceClient()

    response = node.send_request(5, 8)

    node.get_logger().info(f'Resultado: {response.sum}')

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()