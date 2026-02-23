import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Publisher(Node):
    def __init__(self):
        super().__init__('publisher')

        self.declare_parameter('topic_name', '/spgc/receiver')
        self.declare_parameter('text', 'Hello, ROS2!')

        topic_name = self.get_parameter('topic_name').get_parameter_value().string_value
        self._publisher = self.create_publisher(String, topic_name, 10)

        self._timer = self.create_timer(1.0, self._on_timer)

        self.get_logger().info(f'Publishing to: {topic_name}')

        # Publish immediately on startup
        self._on_timer()

    def _on_timer(self):
        text = self.get_parameter('text').get_parameter_value().string_value
        msg = String()
        msg.data = text
        self._publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = Publisher()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()