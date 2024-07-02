// src/image_publisher.cpp

#include <rclcpp/rclcpp.hpp>
#include <sensor_msgs/msg/image.hpp>
#include <opencv2/opencv.hpp>
#include <cv_bridge/cv_bridge.hpp>

class ImagePublisher : public rclcpp::Node
{
public:
    ImagePublisher() : Node("image_publisher")
    {
        publisher_ = this->create_publisher<sensor_msgs::msg::Image>("video_frames", 10);
        timer_ = this->create_wall_timer(
            std::chrono::milliseconds(1000),
            std::bind(&ImagePublisher::timer_callback, this));
        
        cap_.open(0);  // Open the default camera
        if (!cap_.isOpened()) {
            RCLCPP_ERROR(this->get_logger(), "Failed to open camera");
        }
    }

private:
    void timer_callback()
    {
        cv::Mat frame;
        cap_ >> frame;
        if (!frame.empty()) {
            // cv::resize(frame, frame, cv::Size(100, 50));
            auto msg = cv_bridge::CvImage(std_msgs::msg::Header(), "bgr8", frame).toImageMsg();
            publisher_->publish(*msg);
            RCLCPP_INFO(this->get_logger(), "Publishing video frame");
        } else {
            RCLCPP_WARN(this->get_logger(), "Captured empty frame");
        }
    }

    rclcpp::Publisher<sensor_msgs::msg::Image>::SharedPtr publisher_;
    rclcpp::TimerBase::SharedPtr timer_;
    cv::VideoCapture cap_;
};

int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<ImagePublisher>());
    rclcpp::shutdown();
    return 0;
}
