from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration, PythonExpression
from launch.conditions import IfCondition
from launch_ros.actions import Node
from launch.actions import SetEnvironmentVariable, IncludeLaunchDescription, TimerAction, RegisterEventHandler, DeclareLaunchArgument
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
import launch_ros.actions
import os

def generate_launch_description():
    ros_gz_sim_pkg_path = get_package_share_directory('ros_gz_sim')
    sim_pkg_path = FindPackageShare('simulation_package')
    gz_launch_path = PathJoinSubstitution([ros_gz_sim_pkg_path, 'launch', 'gz_sim.launch.py'])

    config_controller = os.path.join(get_package_share_directory('wg_navigation'), 'params', 'controller_manager.yaml')
    wallg_urdf = os.path.join(get_package_share_directory('wg_navigation'),'URDF', 'URDF_ASSEMBLY.urdf')

    launch_dir = os.path.join(get_package_share_directory('wg_bringup'), 'launch')

    mode = LaunchConfiguration('mode')

    mode_arg = DeclareLaunchArgument('mode', 
                          default_value='sim',
                          description="Launch argument som bestemme om vi kjøre simulasjon eller ikke."
                          )


    startup_node = Node(
        package='wg_bringup',
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
        condition=IfCondition(PythonExpression(["'", mode, "' == 'sim'"])),    #   ' er en separator i et python-uttrykk objekt
        output='screen'
    )
    
    wrapper_node = Node(
        package='wg_yolo_package',
        executable='yolo_wrapper.sh',
        name='ros_yolo_node',
        output='screen'

    )

    gz_start_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gz_launch_path),
        launch_arguments={
            'gz_args': PathJoinSubstitution([sim_pkg_path, 'gazebo_includes', 'worlds/example.sdf']), 
            'on_exit_shutdown': 'True'
        }.items(),
        condition=IfCondition(PythonExpression(["'", mode, "' == 'sim'"])),
    )

    picamera_node = Node(
        package='wg_picamera',
        executable='wg_picamera_exec',
        name='picamera_node',
        output='screen',
        condition=IfCondition(PythonExpression(["'", mode, "' == 'real'"])),
    )

    navigation_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(launch_dir, 'Nav2_bringup.py')
        ),
        condition=IfCondition(PythonExpression(["'", mode, "' == 'real'"])),
        launch_arguments={
            'namespace': '',
            'use_sim_time': 'false',
            'autostart': 'true',
            'use_respawn': 'false',
            'rviz_config_file': os.path.join(get_package_share_directory('wg_navigation'), 'params', 'nav2_params_wallg.yaml')
        }.items(),
    )

    navigation_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(launch_dir, 'Nav2_bringup.py')
        ),
        condition=IfCondition(PythonExpression(["'", mode, "' == 'real'"])),
        launch_arguments={
            'namespace': '',
            'use_sim_time': 'false',
            'autostart': 'true',
            'use_respawn': 'false',
            'rviz_config_file': os.path.join(get_package_share_directory('wg_navigation'), 'params', 'nav2_params_wallg.yaml')
        }.items(),
    )

    with open(wallg_urdf, 'r') as infp:
        robot_desc = infp.read()

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_desc
        }]
    )

    ldlidar_node = Node(
        package='ldlidar_ros2',
        executable='ldlidar_ros2_node',
        name='ldlidar_publisher_ld06',
        output='screen',
        parameters=[
            {'product_name': 'LDLiDAR_LD06'},
            {'laser_scan_topic_name': 'scan'},
            {'point_cloud_2d_topic_name': 'pointcloud2d'},
            {'frame_id': 'base_laser'},
            {'port_name': '/dev/ttyAMA0'},
            {'serial_baudrate': 230400},
            {'laser_scan_dir': True},
            {'enable_angle_crop_func': False},
            {'angle_crop_min': 135.0},  # unit is degress
            {'angle_crop_max': 225.0},  # unit is degress
            {'range_min': 0.02}, # unit is meter
            {'range_max': 12.0}   # unit is meter
      ]
    )

    ros2_control_manager = Node(
        package='controller_manager',
        executable='ros2_control_node',
        name='ros2_control',
        parameters=[{
            'robot_description': robot_desc,
            'params_file': config_controller,
            }],
        output='screen',
    )

    delayed_controller = TimerAction(period=3.0,
                                     actions=[ros2_control_manager])
    
    diff_drive_spawner = Node(
        package='controller_manager',
        executable='spawner.py',
        arguments=['joint_group_velocity_controller'],
    )

    delayed_diff_spawner = RegisterEventHandler(
                            OnProcessExit(
                                target_action=ros2_control_manager,
                                on_start=[diff_drive_spawner],
                            )
    )

    joint_broad_spawner = Node(
        package='controller_manager',
        executable='spawner.py',
        arguments=['joint_state_broadcaster']
    )

    delayed_joint_spawner = RegisterEventHandler(
                            OnProcessExit(
                                target_action=ros2_control_manager,
                                on_start=[joint_broad_spawner],
                            )
    )

    gui_node = Node(
        package='wg_controller_gui',
        executable='controller_gui_exec',
        name='gui_node',
        output='screen',
        condition=IfCondition(PythonExpression(["'", mode, "' == 'real'"])),
    )

    wait_nav2_node = TimerAction(period=2.0,
                                 actions=[navigation_node])
    
    wait_sec_node = TimerAction(period=2.0,
                                actions=[   gz_start_node,
                                            bridge_node,
                                            ldlidar_node,
                                            robot_state_publisher_node,
                                            delayed_controller,
                                            delayed_diff_spawner,
                                            delayed_joint_spawner,
                                            #wait_nav2_node,
                                            #wrapper_node,
                                            #picamera_node,
                                            #gui_node,
                                            ])


    return LaunchDescription([
        SetEnvironmentVariable(
            'GZ_SIM_RESOURCE_PATH',
            PathJoinSubstitution([sim_pkg_path, 'gazebo_includes', 'models'])
        ),
        SetEnvironmentVariable(
            'BNL_VENV_PATH',os.path.expandvars('/home/${USER}/.BNL_venv') 
        ),
        SetEnvironmentVariable(
            'ROS_DOMAIN_ID','81'
        ),

        mode_arg,
        startup_node,

        RegisterEventHandler(
            OnProcessExit(
                target_action=startup_node,
                on_exit=[wait_sec_node]
            )
        ),

    ])