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
        ('share/' + package_name + '/params', glob('params/*.*', recursive=True)),
        ('share/' + package_name + '/URDF', glob("params/URDF/meshes/*", recursive=True)),
        ('share/' + package_name + '/URDF', ["params/URDF/URDF_ASSEMBLY.urdf"]),

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
