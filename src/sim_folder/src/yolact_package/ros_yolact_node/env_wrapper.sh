#!/usr/bin/env bash

set -e

venv_path="${BNL_VENV_PATH}"

source "${BNL_VENV_PATH}/bin/activate"

exec python -m "ros_yolact_node.entrypoint" "$@"
