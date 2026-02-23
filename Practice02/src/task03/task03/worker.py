import rclpy
from rclpy.node import Node

# from std_msgs.msg import String
from std_srvs.srv import Trigger


class Worker(Node):
    def __init__(self):
        super().__init__("worker")

        # parameters
        self.declare_parameter("service_name", "/trigger_service")
        self.declare_parameter("default_string", "No service available")

        service_name = (
            self.get_parameter("service_name").get_parameter_value().string_value
        )
        default_string = (
            self.get_parameter("default_string").get_parameter_value().string_value
        )

        self._stored_string = default_string
        spgc_service_name = "/spgc/trigger"
        client = self.create_client(Trigger, spgc_service_name)
        if client.wait_for_service(timeout_sec=1.0):
            req = Trigger.Request()
            future = client.call_async(req)
            try:
                rclpy.spin_until_future_complete(self, future, timeout_sec=1.0)
            except Exception:
                future = None
            if future is not None and future.done() and future.result() is not None:
                res = future.result()
                if hasattr(res, "message"):
                    self._stored_string = res.message

        self._service = self.create_service(Trigger, service_name, self._handle_trigger)

        # self._publisher = self.create_publisher(String, "/spgc/receiver", 10)

    def _handle_trigger(self, request, response):
        response.success = True
        response.message = self._stored_string
        return response


def main(args=None):
    rclpy.init(args=args)
    node = Worker()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
