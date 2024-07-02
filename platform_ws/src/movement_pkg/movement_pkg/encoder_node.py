import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool, UInt32
from platform_interfaces.msg import SteeringSignal
from time import sleep
import lgpio
# import gpiod


class ENCODERNode(Node):
    def __init__(self):
        super().__init__("encoder_node")
        self.get_logger().info("inited node")
        self.R_H1_PIN = 12
        self.R_H2_PIN = 16
        # self.speed_signal_pub = self.create_publisher(SteeringSignal, "motor_speed_signal", 0)
        self.h = lgpio.gpiochip_open(4)
        lgpio.gpio_claim_input(self.h, self.R_H1_PIN)
        lgpio.gpio_claim_input(self.h, self.R_H2_PIN)
        self.get_logger().info("inited")
        self.last_h1 = lgpio.gpio_read(self.h, self.R_H1_PIN)
        self.last_h2 = lgpio.gpio_read(self.h, self.R_H2_PIN)
        self.encode_counter = 0
        self.iter_counter = 0
        self.direction = True #forward is true
        self.encode_timer = self.create_timer(0.000001, self.update_counter)
        self.publish_timer = self.create_timer(0.1, self.update_speed)

    def update_speed(self):
        self.get_logger().info(f"speed: {self.encode_counter/self.iter_counter}, dir: {str(self.direction)}")
        self.encode_counter = 0
        self.iter_counter = 0
        
    def update_counter(self):
        self.iter_counter += 1
        self.encode_counter += self.get_encode()

    def get_encode(self):
        h1 = lgpio.gpio_read(self.h, self.R_H1_PIN)
        h2 = lgpio.gpio_read(self.h, self.R_H2_PIN)
        if h1 == True:
            if h1 == self.last_h1 and h2 == self.last_h2:
                self.last_h1 = h1
                self.last_h2 = h2
                return 0
            if self.last_h2 == 0 and h2 == 1:
                if h1==0 and self.direction:
                    self.direction = False
                else:
                    if h1 == 1 and not self.direction:
                        self.direction == True

            self.last_h1 = h1
            self.last_h2 = h2
            if self.direction:
                return -1
            return 1
        else:
            return 0




    # def get_encode(self):
    #     h1 = lgpio.gpio_read(self.h, self.R_H1_PIN)
    #     h2 = lgpio.gpio_read(self.h, self.R_H2_PIN)
    #     if h1 == self.last_h1 and h2 == self.last_h2:
    #         self.last_h1 = h1
    #         self.last_h2 = h2
    #         return 0
    #     self.last_h1 = h1
    #     self.last_h2 = h2
    #     if h1 ==1 and h2 == 0:
    #         return 1
    #     return -1


    def __del__(self):
        lgpio.gpiochip_close(self.h)


def main(args=None):
	rclpy.init(args=args)
	node = ENCODERNode()
	rclpy.spin(node)
	node.destroy_node()
	rclpy.shutdown()

if __name__ == "__main__":
	main()
