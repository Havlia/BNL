// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from interface:msg/Zero.idl
// generated code does not contain a copyright notice

#include "interface/msg/detail/zero__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_interface
const rosidl_type_hash_t *
interface__msg__Zero__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xa4, 0x52, 0x6b, 0xe0, 0x4a, 0x47, 0x5d, 0x9a,
      0xc3, 0x21, 0x96, 0xb8, 0xf8, 0x5e, 0x26, 0xea,
      0x05, 0x75, 0x2d, 0x62, 0x8d, 0xfd, 0xf5, 0xb8,
      0x02, 0x9c, 0x36, 0xa5, 0x9c, 0x50, 0x27, 0x31,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types

// Hashes for external referenced types
#ifndef NDEBUG
#endif

static char interface__msg__Zero__TYPE_NAME[] = "interface/msg/Zero";

// Define type names, field names, and default values
static char interface__msg__Zero__FIELD_NAME__structure_needs_at_least_one_member[] = "structure_needs_at_least_one_member";

static rosidl_runtime_c__type_description__Field interface__msg__Zero__FIELDS[] = {
  {
    {interface__msg__Zero__FIELD_NAME__structure_needs_at_least_one_member, 35, 35},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_UINT8,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
interface__msg__Zero__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {interface__msg__Zero__TYPE_NAME, 18, 18},
      {interface__msg__Zero__FIELDS, 1, 1},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "# bare en placeholder fil intil videre";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
interface__msg__Zero__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {interface__msg__Zero__TYPE_NAME, 18, 18},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 39, 39},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
interface__msg__Zero__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *interface__msg__Zero__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}
