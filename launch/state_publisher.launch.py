from ament_index_python import get_package_share_directory
import launch
import os
from launch.substitutions import Command, LaunchConfiguration
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import PythonExpression
import launch_ros
from launch_ros.descriptions import ParameterValue

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time')
    default_model_path = os.path.join(get_package_share_directory('ugv_description'), 'models/urdf/ugv_description.xacro')
    
    # Robot state publisher for simulation (when use_sim_time is True)
    robot_state_publisher_sim = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'use_sim_time': use_sim_time,
            'robot_description': ParameterValue(Command(['xacro ', LaunchConfiguration('model')]), value_type=str)
        }],
        condition=IfCondition(use_sim_time)
    )
    
    # Robot state publisher for real robot (when use_sim_time is False)
    
    joint_state_publisher_node = launch_ros.actions.Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        parameters=[{'use_sim_time': use_sim_time}],
    )
    
    return launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument(
            name='use_sim_time', 
            default_value='True',
            description='Flag to enable use_sim_time'
        ),
        launch.actions.DeclareLaunchArgument(
            name='model', 
            default_value=default_model_path,
            description='Absolute path to robot urdf file (used only when use_sim_time is True)'
        ),
        robot_state_publisher_sim,
        joint_state_publisher_node
    ])