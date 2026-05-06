#!/usr/bin/env bash

set -e

venv_path="${BNL_VENV_PATH}"

source "${BNL_VENV_PATH}/.venv/bin/activate"

exec python3 -m "ros_yolo_node.ros_yolo_code" "$@"
