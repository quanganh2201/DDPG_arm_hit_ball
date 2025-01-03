import os
from launch_ros.actions import Node
from launch import LaunchDescription
from launch.substitutions import Command
from launch.actions import ExecuteProcess
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # Chọn mô hình robot
    robot_model = 'a0912'
    # robot_model = 'm1013'

    xacro_file = get_package_share_directory('my_doosan_pkg') + '/description' + '/xacro/' + robot_model + '.urdf.xacro'

    # Robot State Publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='both',
        parameters=[{'robot_description': Command(['xacro', ' ', xacro_file])}]
    )

    # Spawn the robot in Gazebo
    spawn_entity_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-entity', 'my_doosan_robot', '-topic', 'robot_description'],
        output='screen'
    )
    # Gazebo   

    world_file_name = 'my_empty_world.world'
    world = os.path.join(get_package_share_directory('my_doosan_pkg'), 'worlds', world_file_name)
    gazebo_node = ExecuteProcess(cmd=['gazebo', '--verbose', world,'-s', 'libgazebo_ros_factory.so'], output='screen')



    # RViz
    rviz_config_file = get_package_share_directory('my_doosan_pkg') + "/rviz/view_config.rviz"
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='log',
        arguments=['-d', rviz_config_file]
    )

    # Load và khởi động các controller cho vận tốc
    load_joint_state_broadcaster = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active', 'joint_state_broadcaster'],
        output='screen'
    )

    # Load controller điều khiển vận tốc
    load_velocity_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active', 'joint_velocity_controller'],
        output='screen'
    )

    return LaunchDescription([
        robot_state_publisher,
        spawn_entity_robot,
        gazebo_node,
        load_joint_state_broadcaster,
        load_velocity_controller,
        rviz_node
        
    ])
