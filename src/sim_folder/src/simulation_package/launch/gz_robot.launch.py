from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.actions import SetEnvironmentVariable, IncludeLaunchDescription, TimerAction, RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
import os

def generate_launch_description():
    ros_gz_sim_pkg_path = get_package_share_directory('ros_gz_sim')
    sim_pkg_path = FindPackageShare('simulation_package')
    gz_launch_path = PathJoinSubstitution([ros_gz_sim_pkg_path, 'launch', 'gz_sim.launch.py'])


    startup_node = Node(
        package='yolact_package',
        executable='bnl_startup.sh',
        name='BNL_startup',
        output='screen',
        emulate_tty=True

    )

    # Bridging and remapping Gazebo topics to ROS 2 (replace with your own topics)
    bridge_node = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=['/scan_gpu@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
                    '/camera_image@sensor_msgs/msg/Image[gz.msgs.Image'],
        output='screen'
    )
    
    wrapper_node = Node(
        package='yolact_package',
        executable='env_wrapper.sh',
        name='ros_yolact_node',
        output='screen'

    )

    gz_start_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gz_launch_path),
        launch_arguments={
            'gz_args': PathJoinSubstitution([sim_pkg_path, 'gazebo_includes', 'worlds/example.sdf']), 
            'on_exit_shutdown': 'True'
        }.items()
    )

    return LaunchDescription([
        SetEnvironmentVariable(
            'GZ_SIM_RESOURCE_PATH',
            PathJoinSubstitution([sim_pkg_path, 'gazebo_includes', 'models'])
        ),
        SetEnvironmentVariable(
            'BNL_VENV_PATH',os.path.expanduser('~/.BNL_venv/.venv') 
        ),
        SetEnvironmentVariable(
            'CUDA_VISIBLE_DEVICES',""
        ),

        startup_node,

        RegisterEventHandler(
            OnProcessExit(
                target_action=startup_node,
                on_exit=[gz_start_node,
                         bridge_node,
                         wrapper_node]
            )
        )
    ])