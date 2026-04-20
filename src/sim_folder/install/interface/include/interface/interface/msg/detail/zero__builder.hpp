// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from interface:msg/Zero.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "interface/msg/zero.hpp"


#ifndef INTERFACE__MSG__DETAIL__ZERO__BUILDER_HPP_
#define INTERFACE__MSG__DETAIL__ZERO__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "interface/msg/detail/zero__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace interface
{

namespace msg
{


}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::interface::msg::Zero>()
{
  return ::interface::msg::Zero(rosidl_runtime_cpp::MessageInitialization::ZERO);
}

}  // namespace interface

#endif  // INTERFACE__MSG__DETAIL__ZERO__BUILDER_HPP_
