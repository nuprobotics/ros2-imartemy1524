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

        self._text = self.get_parameter('text').get_parameter_value().string_value

        self._pub = self.create_publisher(String, topic_name, 10)
        self.create_timer(0.1, self._publish)
        self._publish()
    def _publish(self):
        msg = String()
        msg.data = self._text
        self._pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = Publisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()