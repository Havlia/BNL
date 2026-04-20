#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "interface__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__interface__msg__Zero() -> *const std::ffi::c_void;
}

#[link(name = "interface__rosidl_generator_c")]
extern "C" {
    fn interface__msg__Zero__init(msg: *mut Zero) -> bool;
    fn interface__msg__Zero__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Zero>, size: usize) -> bool;
    fn interface__msg__Zero__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Zero>);
    fn interface__msg__Zero__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Zero>, out_seq: *mut rosidl_runtime_rs::Sequence<Zero>) -> bool;
}

// Corresponds to interface__msg__Zero
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// bare en placeholder fil intil videre

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Zero {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for Zero {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !interface__msg__Zero__init(&mut msg as *mut _) {
        panic!("Call to interface__msg__Zero__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Zero {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interface__msg__Zero__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interface__msg__Zero__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interface__msg__Zero__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Zero {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Zero where Self: Sized {
  const TYPE_NAME: &'static str = "interface/msg/Zero";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__interface__msg__Zero() }
  }
}


