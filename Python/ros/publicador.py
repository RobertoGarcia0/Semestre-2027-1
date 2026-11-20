import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
class PublisherNode(Node):
    def __init__(self):
        super().__init__('publisher_node')
        self.publisher = self.create_publisher(Int32, '/contador', 10)
        self.counter = 0
        self.timer = self.create_timer(1.0, self.publish_message)

    def publish_message(self):
        msg = Int32()
        msg.data = self.counter
        self.publisher.publish(msg)
        self.get_logger().info(f'Publicado: {msg.data}')
        self.counter += 1

def main(args=None):
    rclpy.init(args=args)
    node = PublisherNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()