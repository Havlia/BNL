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
    
    nav2_launch_path = os.path.join(get_package_share_directory('nav2_bringup'), 'launch', 'bringup_launch.py')
    nav2_rviz_path = os.path.join(get_package_share_directory('nav2_bringup'), 'launch', 'rviz_launch.py')

    explorer_config = os.path.join(get_package_share_directory("explore_lite"), "config", "params.yaml")
    wallg_urdf_path = os.path.join(get_package_share_directory('wg_navigation'), 'params', 'wall_g.urdf')
    nav2_params = os.path.join(get_package_share_directory('wg_navigation'), 'params', 'nav2_params_wallg.yaml')
    rviz_config = os.path.join(get_package_share_directory('wg_navigation'), 'params', 'rviz_config_wallg.rviz')

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

    nav2_launch_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(nav2_launch_path),
        launch_arguments={
            'namespace': '',
            'use_sim_time': 'False',
            'autostart': 'True',
            'slam': 'True',
            'rviz': 'True',
            'params_file': nav2_params,
        }.items(),
        condition=IfCondition(PythonExpression(["'", mode, "' == 'real'"])),

    )
    
    with open(wallg_urdf_path, 'r') as infp:
        robot_desc = infp.read()

    params = {'robot_description': robot_desc}

    robot_state_publisher = launch_ros.actions.Node(package='robot_state_publisher',
                                  executable='robot_state_publisher',
                                  output='both',
                                  parameters=[params])

    explorer_node = Node(
        package="explore_lite",
        name="explore_node",
        namespace='',
        executable="explore",
        parameters=[explorer_config, {"use_sim_time": False}],
        output="screen",
        remappings=[("/tf", "tf"), ("/tf_static", "tf_static")],
    )

    nav2_rviz_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(nav2_rviz_path),
        launch_arguments={
            'namespace': '',
            'use_sim_time': 'False',
            'rviz_config': rviz_config,
        }.items(),
        condition=IfCondition(PythonExpression(["'", mode, "' == 'real'"])),
    )

    gui_node = Node(
        package='wg_controller_gui',
        executable='controller_gui_exec',
        name='gui_node',
        output='screen',
        condition=IfCondition(PythonExpression(["'", mode, "' == 'real'"])),
    )

    wait_sec_node = TimerAction(period=2.0,
                                actions=[   gz_start_node,
                                            bridge_node,
                                            ldlidar_node,
                                            nav2_launch_node,
                                            explorer_node,
                                            robot_state_publisher,
                                            nav2_rviz_node,
                                            #wrapper_node,
                                            #picamera_node,
                                            gui_node])

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
        )
    ])