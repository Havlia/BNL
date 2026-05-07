cmake_minimum_required(VERSION 3.8)
project(wg_bt_translation)

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(pluginlib REQUIRED)
find_package(nav2_behavior_tree REQUIRED)
find_package(behaviortree_cpp_v3 REQUIRED)
find_package(wg_interface REQUIRED)

add_library(wg_bt_translation SHARED
  src/bt_translation.cpp
)

ament_target_dependencies(wg_bt_translation
  rclcpp
  pluginlib
  nav2_behavior_tree
  behaviortree_cpp_v3
  wg_interface
)

pluginlib_export_plugin_description_file(
  nav2_behavior_tree
  plugin.xml
)

install(TARGETS wg_bt_translation
  LIBRARY DESTINATION lib
)

install(DIRECTORY include/
  DESTINATION include
)

install(FILES plugin.xml
  DESTINATION share/${PROJECT_NAME}
)

ament_package()