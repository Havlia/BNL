"""AI-TAMPERED NOTICE (2026-02-17)

This file was created/modified by an AI assistant (GitHub Copilot) to provide a minimal
robot_state_publisher launch.
"""

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description() -> LaunchDescription:
	pkg_share = get_package_share_directory("my_robot_description")
	# AI-TAMPERED NOTICE (2026-02-17): Switched default model to Xacro and
	# generate robot_description by running xacro. The previous test.urdf in this
	# workspace is not valid XML, which caused robot_state_publisher parse errors.
	default_model = f"{pkg_share}/description/urdf/robot.urdf.xacro"

	model = LaunchConfiguration("model")
	robot_description = ParameterValue(Command(["xacro ", model]), value_type=str)

	return LaunchDescription(
		[
			DeclareLaunchArgument(
				"model",
				default_value=default_model,
				description="Absolute path to robot URDF file.",
			),
			# AI-TAMPERED NOTICE (2026-02-17): Added joint_state_publisher so
			# robot_state_publisher can compute transforms for non-fixed joints
			# (e.g., continuous wheel joints). Without /joint_states, RViz shows
			# "No transform from [wheel] to [base_link]".
			Node(
				package="joint_state_publisher",
				executable="joint_state_publisher",
				output="screen",
			),
			Node(
				package="robot_state_publisher",
				executable="robot_state_publisher",
				output="screen",
				parameters=[{"robot_description": robot_description}],
			),
		]
	)
