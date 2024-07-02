import rclpy
from rclpy.node import Node
from time import sleep
import spidev

# import gpiod


class SPIDataNode(Node):
    def __init__(self):
        super().__init__("receive_spi_node")
        self.communication_codes = {"R_abs_position":[0x01],"L_abs_position":[0x02]}
        self.get_logger().info("inited")
        self.Tp = 1
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.max_speed_hz = 7629
        self.publish_timer = self.create_timer(self.Tp, self.timer_callback)


    def timer_callback(self):
        for keycode in self.communication_codes.items():
            key,code = keycode
            received_data = self.spi.xfer(code, 500000, 9000)
            # sleep(0.001)
            self.get_logger().info(f"{str(key)}: {str(received_data)}")
    # def __del__(self):



def main(args=None):
	rclpy.init(args=args)
	node = SPIDataNode()
	rclpy.spin(node)
	node.destroy_node()
	rclpy.shutdown()

if __name__ == "__main__":
	main()
