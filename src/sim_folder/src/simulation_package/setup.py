from setuptools import find_packages, setup
from glob import glob

package_name = 'simulation_package'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/'+ package_name + '/launch', glob('launch/*.launch.py')),
        ('share/' + package_name + '/gazebo_includes/models', glob('gazebo_includes/models/**/*', recursive=True)),
        ('share/' + package_name + '/gazebo_includes/plugins', glob('gazebo_includes/plugins/**/*', recursive=True)),
        ('share/' + package_name + '/gazebo_includes/worlds', glob('gazebo_includes/worlds/**/*', recursive=True)),
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
    scripts=['scripts/create_urdf.sh']
)
