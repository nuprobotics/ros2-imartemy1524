import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger


class Worker(Node):
    def __init__(self):
        super().__init__("publisher")

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

        self._service = self.create_service(Trigger, service_name, self._handle_trigger)

        self._client = self.create_client(Trigger, "/spgc/trigger")

        self._timer = self.create_timer(0.1, self._call_spgc_trigger)

    def _call_spgc_trigger(self):
        try:
            if self._client.wait_for_service(timeout_sec=1.0):
                req = Trigger.Request()
                future = self._client.call_async(req)
                rclpy.spin_until_future_complete(self, future, timeout_sec=1.0)
                if future is not None and future.done():
                    res = future.result()
                    if res is not None and hasattr(res, "message"):
                        self._stored_string = res.message
        finally:
            try:
                self._timer.cancel()
            except Exception:
                pass

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
