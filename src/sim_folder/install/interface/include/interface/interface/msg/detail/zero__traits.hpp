// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from interface:msg/Zero.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "interface/msg/zero.hpp"


#ifndef INTERFACE__MSG__DETAIL__ZERO__TRAITS_HPP_
#define INTERFACE__MSG__DETAIL__ZERO__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "interface/msg/detail/zero__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace interface
{

namespace msg
{

inline void to_flow_style_yaml(
  const Zero & msg,
  std::ostream & out)
{
  (void)msg;
  out << "null";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Zero & msg,
  std::ostream & out, size_t indentation = 0)
{
  (void)msg;
  (void)indentation;
  out << "null\n";
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Zero & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace interface

namespace rosidl_generator_traits
{

[[deprecated("use interface::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const interface::msg::Zero & msg,
  std::ostream & out, size_t indentation = 0)
{
  interface::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use interface::msg::to_yaml() instead")]]
inline std::string to_yaml(const interface::msg::Zero & msg)
{
  return interface::msg::to_yaml(msg);
}

template<>
inline const char * data_type<interface::msg::Zero>()
{
  return "interface::msg::Zero";
}

template<>
inline const char * name<interface::msg::Zero>()
{
  return "interface/msg/Zero";
}

template<>
struct has_fixed_size<interface::msg::Zero>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<interface::msg::Zero>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<interface::msg::Zero>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // INTERFACE__MSG__DETAIL__ZERO__TRAITS_HPP_
