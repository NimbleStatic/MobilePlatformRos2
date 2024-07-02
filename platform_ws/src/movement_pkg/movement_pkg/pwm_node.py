import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool, UInt32
from platform_interfaces.msg import SteeringSignal
from time import sleep
import lgpio
# import gpiod


class PWMNode(Node):
    def __init__(self):
        super().__init__("pwm_node")
        self.get_logger().info("inited node")
        self.PWM_FREQ = 500
        self.R_FORW_PIN = 14
        self.R_BACK_PIN = 15
        self.speed_signal_sub = self.create_subscription(SteeringSignal, "motor_speed_signal", self.steering_callback, 0)
        self.h = lgpio.gpiochip_open(4)
        lgpio.gpio_claim_output(self.h, self.R_FORW_PIN)
        lgpio.gpio_claim_output(self.h, self.R_BACK_PIN)

        
        # lgpio.tx_pwm(self.h, self.R_FORW_PIN, self.PWM_FREQ, 50)
        self.get_logger().info("inited")
        self.current_i = -100
        self.set_r_motor_signal(0)
        self.timer = self.create_timer(1, self.timer_callback)

    def timer_callback(self):
        self.get_logger().info("Timer callback triggered")
        self.current_i += 1
        if self.current_i > 100:
        	self.current_i = -100
        # lgpio.tx_pwm(self.h, self.R_FORW_PIN, self.PWM_FREQ, self.current_i)
        self.set_r_motor_signal(self.current_i)
        self.get_logger().info(f"pwm: {self.current_i}")

    def steering_callback(self, msg:SteeringSignal):
        self.get_logger().info("received signal")
        s_l = msg.left_signal
        s_r = msg.right_signal
        self.set_r_motor_signal(s_r)

    def set_r_motor_signal(self, signal:int):
        signal = min(signal, 100)
        signal = max(signal, -100)
        signal_strength = abs(signal)
        if signal >0:
            lgpio.tx_pwm(self.h, self.R_FORW_PIN, self.PWM_FREQ, signal_strength)
            lgpio.tx_pwm(self.h, self.R_BACK_PIN, self.PWM_FREQ, 0)
        else:
            lgpio.tx_pwm(self.h, self.R_FORW_PIN, self.PWM_FREQ, 0)
            lgpio.tx_pwm(self.h, self.R_BACK_PIN, self.PWM_FREQ, signal_strength)



    def __del__(self):
        lgpio.tx_pwm(self.h, self.R_FORW_PIN, self.PWM_FREQ, 0)
        lgpio.tx_pwm(self.h, self.R_BACK_PIN, self.PWM_FREQ, 0)

        lgpio.gpiochip_close(self.h)


def main(args=None):
	rclpy.init(args=args)
	node = PWMNode()
	rclpy.spin(node)
	node.destroy_node()
	rclpy.shutdown()

if __name__ == "__main__":
	main()

# LED = 23
        
        # # open the gpio chip and set the LED pin as output
        # h = lgpio.gpiochip_open(4)
        # lgpio.gpio_claim_output(h, LED)
        
        # try:
        #     while True:
        #         # Turn the GPIO pin on
        #         lgpio.gpio_write(h, LED, 1)
        #         self.get_logger().info(f"turned on pin {LED}")

        #         sleep(1)
        
        #         # Turn the GPIO pin off
        #         lgpio.gpio_write(h, LED, 0)
        #         self.get_logger().info(f"turned off pin {LED}")

        #         sleep(1)
                
        # except KeyboardInterrupt:
        #     lgpio.gpio_write(h, LED, 0)
        #     lgpio.gpiochip_close(h)