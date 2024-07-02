cmake_minimum_required(VERSION 3.5)
project(cpp_package)

# Default to C++14
set (CMAKE_CXX_STANDARD 11)

# find dependencies

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(cv_bridge REQUIRED)
find_package(OpenCV REQUIRED)

include_directories(
  ${cv_bridge_INCLUDE_DIRS}
)

add_executable(image_publisher src/camera_pub.cpp)
ament_target_dependencies(image_publisher rclcpp sensor_msgs cv_bridge OpenCV)

install(TARGETS
  image_publisher
  DESTINATION lib/${PROJECT_NAME})

ament_package()
