from setuptools import find_packages, setup
import glob

package_name = 'wg_controller_gui'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name, ['assets/icons/bnl_logo.svg', 'assets/icons/bnl_logo.png'])
        #('lib/' + package_name, glob.glob('assets/**/*.svg', recursive=True))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='lillehavard',
    maintainer_email='haavaali@stud.ntnu.no',
    description='TODO: Package description',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'controller_gui_exec = wg_controller_gui.controller_gui:main'
        ],
    },
)
