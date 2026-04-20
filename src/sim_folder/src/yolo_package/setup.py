from setuptools import find_packages, setup

package_name = 'yolo_package'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/segmentation_model', ['ros_yolo_node/segmentation_model/yolo26n.pt'])
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
        ],
    },
    scripts={
        'bnl_startup.sh',
        'ros_yolo_node/yolo_wrapper.sh',
        'ros_yolo_node/HACK_run_topic_list.sh'
    }
)
