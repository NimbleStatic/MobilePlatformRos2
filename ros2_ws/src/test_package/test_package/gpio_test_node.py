import rclpy
from rclpy.node import Node
import RPi.GPIO as gpio
from std_msgs.msg import Bool
from rclpy.callback_groups import ReentrantCallbackGroup

class GPIONode(Node):
	def __init__(self):
		super().__init__("gpio_node")
		self.get_logger().info("inited node")
		self.led_gpio_sub = self.create_subscription(Bool, "led_state", self.led_callback,0)
		self.get_logger().info("inited subscription")
		
		# self.callback_group = ReentrantCallbackGroup()
	

		gpio.setmode(gpio.BCM)
		self.led_pin  = 24
		gpio.setup(self.led_pin , gpio.OUT)

		gpio.output(self.led_pin , gpio.HIGH)

		self.get_logger().info("inited")

	def led_callback(self, msg:Bool):
		self.get_logger().info(f"got a bool! {str(msg)}")
		state = msg.data
		if state == True:
			pin_state = gpio.HIGH
		else:
			pin_state = gpio.LOW

		gpio.output(self.led_pin , pin_state)
		self.get_logger().info("done job boiss")

	def __del__(self):
		gpio.cleanup()


def main(args=None):
	rclpy.init(args=args)
	node = GPIONode()
	rclpy.spin(node)
	node.destroy_node()
	rclpy.shutdown()

if __name__ == "__main__":
	main()

