import rclpy
from rclpy.node import Node
import RPi.GPIO as gpio
from std_msgs.msg import Bool, UInt32
from rclpy.callback_groups import ReentrantCallbackGroup
from time import sleep

class PWMNode(Node):
	def __init__(self):
		super().__init__("pwm_node")
		self.get_logger().info("inited node")
		self.frec_sub = self.create_subscription(UInt32, "freq_pwm", self.change_frequency, 0)
# pwm.start(50)
		frequency = 100

		gpio.setmode(gpio.BCM)
		self.pwm_pin = 23 #FRONT RIGHT MOTOR, back is 24
		gpio.setup(self.pwm_pin, gpio.OUT)

		self.pwm = gpio.PWM(self.pwm_pin, frequency)
		self.pwm.start(50)
		self.get_logger().info("inited")
		# self.execute()
		self.current_i = 0
		self.timer = self.create_timer(2.0, self.timer_callback)

	def change_frequency(self, msg:UInt32):
		val = msg.data
		self.pwm.ChangeFrequency(val)
		# self.pwm = gpio.PWM(self.pwm_pin, val)
		# self.pwm.start(self.current_i)
		self.get_logger().info(f"changed freq to {val}")

	def timer_callback(self):
		self.get_logger().info("Timer callback triggered")
		self.current_i += 5
		if self.current_i > 100:
			self.current_i = 0
		
		self.pwm.ChangeDutyCycle(self.current_i)
		self.get_logger().info(f"pwm: {self.current_i}")
	# def execute(self):
	# 	while True:
	# 		for i in range(21):
	# 			self.pwm.ChangeDutyCycle(i*5)
	# 			self.get_logger().info(f"pwm: {i*5}")

	# 			sleep(1)

	def __del__(self):
		self.pwm.stop()
		gpio.cleanup()


def main(args=None):
	rclpy.init(args=args)
	node = PWMNode()
	rclpy.spin(node)
	node.destroy_node()
	rclpy.shutdown()

if __name__ == "__main__":
	main()

