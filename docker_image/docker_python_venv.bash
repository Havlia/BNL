python3 -m "venv" "${BNL_VENV_PATH}/.venv" && source "${BNL_VENV_PATH}/.venv/bin/activate"
	pip install --default-timeout=100	cython \
						numpy==1.26.4 \
						cuda-toolkit \
						pillow \
		 				nvidia-cudnn-cu11 \
		 				matplotlib \
		 				picamera2 \
		 				PyQt5 \
		 				PyYAML \
		 				cocotools \
		 				cuda-toolkit \
		 				torch \
		 				torchvision \
		 				ultralytics-opencv-headless 

git clone https://github.com/raspberrypi/libcamera.git

cd libcamera

git checkout v0.5.0+rpt20250429

meson setup build

sudo  ninja -C build

sudo ninja -C build install