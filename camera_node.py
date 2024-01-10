#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import cv2
import numpy as np

class MouseController(Node):

    def __init__(self):
        super().__init__('kontroler')
        self.window_name = "kontroler"
        self.window_size = (512, 700)
        self.cv_image = np.zeros((self.window_size[0], self.window_size[1], 3), np.uint8)
        cv2.imshow(self.window_name, self.cv_image)
        cv2.waitKey(25)
        self.mouse_position = None

        self.publisher = self.create_publisher(Twist, 'cmd_vel', 10)
        self.timer = self.create_timer(0.25, self.timer_callback)
        cv2.setMouseCallback(self.window_name, self.mouse_click_callback)
        print("kontroler wlaczony")

    def timer_callback(self):
        if self.mouse_position is not None:
            cmd_velocity = self.calculate_velocity()
            self.publisher.publish(cmd_velocity)
            self.display_square_at_mouse_position()
        cv2.waitKey(25)

    def calculate_velocity(self):
        cmd_velocity = Twist()
        cmd_velocity.linear.y = 0.0
        velocity = 0.5

        if self.mouse_position[1] < self.window_size[0] / 2:
            cmd_velocity.linear.x = velocity
        else:
            cmd_velocity.linear.x = -velocity
            
        self.get_logger().info(f"Publishing: {cmd_velocity.linear.x}")
        return cmd_velocity

    def display_square_at_mouse_position(self):
        self.cv_image = np.zeros((self.window_size[0], self.window_size[1], 3), np.uint8)
        square_size = 50
        color = (0, 255, 0)
        cv2.rectangle(self.cv_image, (self.mouse_position[0] - square_size // 2, self.mouse_position[1] - square_size // 2),
                      (self.mouse_position[0] + square_size // 2, self.mouse_position[1] + square_size // 2), color, -1)
        cv2.imshow(self.window_name, self.cv_image)

    def mouse_click_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.mouse_position = (x, y)

def main(args=None):
    rclpy.init(args=args)
    kontroler = MouseController()
    rclpy.spin(kontroler)
    kontroler.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
