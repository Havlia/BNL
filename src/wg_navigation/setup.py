from setuptools import find_packages, setup
from glob import glob

package_name = 'wg_navigation'

#print(iglob("params/URDF/*"))

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/params', [  'params/nav2_params_wallg.yaml', 
                                                'params/wall_g.urdf',
                                                'params/rviz_config_wallg.rviz',]),
        ('share/' + package_name + '/URDF', glob("params/URDF/meshes/**/*", recursive=True)),
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
)
