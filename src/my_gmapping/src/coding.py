#!/usr/bin/env python

import rospy
import rosbag
from geometry_msgs.msg import TransformStamped
from sensor_msgs.msg import LaserScan
import tf2_ros
import tf_conversions
import tf2_msgs

rospy.init_node('coding')

file = open('/home/vboxuser/catkin_ws/src/my_gmapping/src/examp3.txt', 'r')


bag = rosbag.Bag('data_gmapping.bag', 'w')


tf_broadcaster = tf2_ros.TransformBroadcaster()
tf_buffer = tf2_ros.Buffer()

count = 1

for line in file:

    odom_data = line.split(';')[0]
    lidar_data = line.split(';')[1]
    timestamp = count
    count += 1
    x = float(odom_data.split(',')[0])
    y = float(odom_data.split(',')[1])
    yaw = float(odom_data.split(',')[2])


    transform_stamped = TransformStamped()
    transform_stamped.header.stamp = rospy.Time.from_sec(timestamp)
    transform_stamped.header.frame_id = 'odom'
    transform_stamped.child_frame_id = 'base_link'
    transform_stamped.transform.translation.x = x
    transform_stamped.transform.translation.y = y
    transform_stamped.transform.translation.z = 0.0
    quaternion = tf_conversions.transformations.quaternion_from_euler(0, 0, yaw)
    transform_stamped.transform.rotation.x = quaternion[0]
    transform_stamped.transform.rotation.y = quaternion[1]
    transform_stamped.transform.rotation.z = quaternion[2]
    transform_stamped.transform.rotation.w = quaternion[3]


    tf_broadcaster.sendTransform(transform_stamped)
    tf_buffer.set_transform(transform_stamped, 'default_authority')
    tf_msg = tf2_msgs.msg.TFMessage()
    tf_msg.transforms.append(transform_stamped)


    scan = LaserScan()
    scan.header.stamp = rospy.Time.from_sec(timestamp)
    scan.header.frame_id = 'base_link'
    scan.angle_min = -2.094
    scan.angle_max = 2.094
    scan.angle_increment = 0.3524
    scan.time_increment = 0.1
    scan.scan_time = 0.1
    scan.range_min = 0.0
    scan.range_max = 5.6
    scan.ranges = [float(x) for x in lidar_data.split(',')]

    rospy.loginfo(scan)
    bag.write("/tf", tf_msg, rospy.Time.from_sec(timestamp))
    bag.write('/base_scan', scan, rospy.Time.from_sec(timestamp))

file.close()
bag.close()
