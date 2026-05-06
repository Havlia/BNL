#!/usr/bin/env bash

set -e

venv_path="${BNL_VENV_PATH}"

source "${BNL_VENV_PATH}/.venv2/bin/activate"

exec python3 -m "wg_test_pwm.pwm_code" "$@"
