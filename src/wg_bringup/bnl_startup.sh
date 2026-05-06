#!/usr/bin/env bash

set -e

#Startup script for Prosjektet med både globale variabla og Virtuelt environment handling:

BNL_VENV_PATH="/home/${USER}/.BNL_venv"

clean() {
	exit_code="$?"
	echo "------------ Environment feilet, sletter filer. Feilkode: ${exit_code} ------------"
	rm -rf "${BNL_VENV_PATH}/.venv"
}

clean2() {
	exit_code="$?"
	
	echo "------------ Environment 2 feilet, sletter filer. Feilkode: ${exit_code} ------------"
	rm -rf "${BNL_VENV_PATH}/.venv2"
	
}

trap clean ERR

if test -d "${BNL_VENV_PATH}/.venv"; then
	echo -e "\033[32mVirtual environment finnes i ${BNL_VENV_PATH}, skipper..\033[0m"
else
	echo -e "\033[31mFinner ikke Venv mappe, bygger...\033[0m" && mkdir -p "${BNL_VENV_PATH}"
	python3 -m venv "${BNL_VENV_PATH}/.venv" && source "${BNL_VENV_PATH}/.venv/bin/activate"
	pip install --no-cache-dir	cython \
					numpy==1.26.4 \
					pillow \
		 			matplotlib \
		 			PyYAML \
		 			cocotools

	pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
	
	pip install --no-cache-dir --no-deps ultralytics-opencv-headless
	
	pip install --no-cache-dir torchvision --index-url https://download.pytorch.org/whl/cpu

	deactivate
	
echo -e "Installed venv in ${BNL_VENV_PATH}"

fi

trap - ERR

trap clean2 ERR

if test -d "${BNL_VENV_PATH}/.venv2"; then
	echo -e "\033[32mVirtual environment 2 finnes i ${BNL_VENV_PATH}, skipper..\033[0m"
else
	echo -e "\033[31mFinner ikke Venv2 mappe, bygger...\033[0m" && mkdir -p "${BNL_VENV_PATH}"
	python3 -m venv "${BNL_VENV_PATH}/.venv2" && source "${BNL_VENV_PATH}/.venv2/bin/activate"
	pip install --no-cache-dir	adafruit-circuitpython-pca9685 \
					adafruit-circuitpython-servokit \
					PyYAML \
					RPi.GPIO \
					numpy
	
	cd ~
	pip3 install adafruit-blinka
	
	sudo raspi-config nonint do_i2c 0
	sudo raspi-config nonint do_spi 0
	deactivate
	
echo -e "Installed venv2 in ${BNL_VENV_PATH}"

fi

trap - ERR

