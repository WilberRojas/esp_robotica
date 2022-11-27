#include <moveit/move_group_interface/move_group_interface.h>
#include <moveit/planning_scene_interface/planning_scene_interface.h>
#include <moveit/planning_interface/planning_interface.h>
#include <moveit/kinematic_constraints/utils.h>

#include <moveit_msgs/DisplayRobotState.h>
#include <moveit_msgs/DisplayTrajectory.h>

#include <moveit_msgs/AttachedCollisionObject.h>
#include <moveit_msgs/CollisionObject.h>

#include <moveit_visual_tools/moveit_visual_tools.h>
#include "ros/ros.h"
#include "std_msgs/Int32.h"
#include "geometry_msgs/PoseStamped.h" /*Geometry message PoseStamped*/



std_msgs::Int32 ack_msg;
int flag=0;
void flagCallback(const std_msgs::Int32::ConstPtr& msg)
{

  flag=msg->data;
}

int main(int argc, char ** argv)
{

    ros::init(argc, argv, "move_group_test");
    ros::NodeHandle node_handle;
    ros::AsyncSpinner spinner(1);
    spinner.start();
	ros::Subscriber sub = node_handle.subscribe("/flag", 10, flagCallback);
	//ros::Publisher ack_pub = node_handle.advertise<std_msgs::Int32>("ack", 10);
	//ros::Rate rate(10);
  static const std::string PLANNING_GROUP = "manipulator"; // most important parameter
  std::vector<double> jv; // Joint values
  std::vector<std::string> jn; // Joint names

  moveit::planning_interface::MoveGroupInterface move_group(PLANNING_GROUP);
  moveit::planning_interface::PlanningSceneInterface planning_scene_interface;
  const robot_state::JointModelGroup* joint_model_group =
  move_group.getCurrentState()->getJointModelGroup(PLANNING_GROUP);

  /** Configure move group **/
  move_group.setPlanningTime(10);
  move_group.setNumPlanningAttempts(20);
  move_group.setGoalPositionTolerance(0.001);
  move_group.setPlannerId("RRTConnectkConfigDefault");

  // Getting Basic Information
  ROS_INFO_NAMED("tutorial", "Reference frame: %s", move_group.getPlanningFrame().c_str());

  // We can also print the name of the end-effector link for this group.
  ROS_INFO_NAMED("tutorial", "End effector link: %s", move_group.getEndEffectorLink().c_str());

  move_group.getCurrentState()->copyJointGroupPositions(joint_model_group, jv);
  jn = joint_model_group->getJointModelNames();
  for (size_t i = 0; i < jv.size(); ++i)
      ROS_INFO("Joint %s: %f", jn[i].c_str(), jv[i]);

	while(ros::ok())
	{
    if(flag==1){

      geometry_msgs::Pose pose;
      pose.orientation.w = 1.0;
      pose.position.x = 0.5;
      pose.position.y = 0.0;
      pose.position.z = 0.3;
      move_group.setPoseTarget(pose);
      move_group.move();
    }

	}


    return 0;
}
