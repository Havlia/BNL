#include <memory>
#include <chrono>
#include <rclcpp/rclcpp.hpp>

#include <behaviortree_cpp_v3/condition_node.h>
#include <behaviortree_cpp_v3/bt_factory.h>

#include "wg_bt_translation/include/bt_translation.hpp"

class FrontierDetectedCondition : public BT::ConditionNode
{
public:
  FrontierDetectedCondition(
    const std::string & name,
    const BT::NodeConfiguration & config)
  : BT::ConditionNode(name, config)
  {
    node_ = config.blackboard
      ->get<rclcpp::Node::SharedPtr>("node");

    client_ = node_->create_client<wg_interface::srv::BearStatus>(
      "bear_discovery");
  }

  BT::NodeStatus tick() override
  {
    auto request =
      std::make_shared<wg_interface::srv::BearStatus::Request>();

    auto future = client_->async_send_request(request);

    auto status = future.wait_for(std::chrono::milliseconds(100));

    if (status != std::future_status::ready) {
      return BT::NodeStatus::FAILURE;
    }

    auto result = future.get();

    if (result->frontier_detected) {
      return BT::NodeStatus::SUCCESS;
    }

    return BT::NodeStatus::FAILURE;
  }

  static BT::PortsList providedPorts()
  {
    return {};
  }

private:
  rclcpp::Node::SharedPtr node_;
  rclcpp::Client<wg_interface::srv::BearStatus>::SharedPtr client_;
};
