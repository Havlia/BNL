#!/usr/bin/env bash

set -e

venv_path="${BNL_VENV_PATH}"

source "${BNL_VENV_PATH}/.venv/bin/activate"

exec python3 -m "wg_picamera.camera_interface" "$@"
