#!/usr/bin/env bash

set -e

#Startup script for Prosjektet med både globale variabla og Virtuelt environment handling:

BNL_VENV_PATH="/home/${USER}/.BNL_venv"

clean() {
	exit_code="$?"
	echo "------------ Environment feilet, sletter filer. Feilkode: ${exit_code} ------------"
	rm -rf "${BNL_VENV_PATH}"
}

trap clean ERR

if test -d "${BNL_VENV_PATH}/.venv"; then
	echo -e "\033[32mVirtual environment finnes i ${BNL_VENV_PATH}, skipper..\033[0m"
else
	echo -e "Finner ikke Venv mappe, bygger..." && mkdir -p "${BNL_VENV_PATH}"
	python3 -m "venv" "${BNL_VENV_PATH}/.venv" && source "${BNL_VENV_PATH}/.venv/bin/activate"
	#pip install	torch torchvision --index-url https://download.pytorch.org/whl/rocm6.0
	pip install	cython \
			cuda-toolkit \
			pillow \
		 	nvidia-cudnn-cu11 \
		 	matplotlib \
		 	PyQt5 \
		 	PyYAML \
		 	cocotools \
		 	opencv-python \
		 	cuda-toolkit \
		 	torch \
		 	torchvision
	deactivate
	
echo -e "Installed venv in ${BNL_VENV_PATH}"

fi

trap - ERR

