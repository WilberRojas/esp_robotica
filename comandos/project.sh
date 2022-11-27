source devel/setup.bash

TEST=$1

if [ "$TEST" != "" ]; then
    a='TEST'
    b=$1
    c="${a} ${b}"
    echo "${c}"
fi

if [ "$TEST" == "goalA" ]; then
   
   roslaunch project_pkg project.launch test:=A detection:=person aruco:=17

elif [ "$TEST" == 'goalB' ]; then
    roslaunch project_pkg project.launch test:=B detection:=person aruco:=29

elif [ "$TEST" == "goalC" ]; then
    roslaunch project_pkg project.launch test:=C detection:=horse aruco:=17

elif [ "$TEST" == "goalD" ]; then
    roslaunch project_pkg project.launch test:=D detection:=horse aruco:=29

else     
    echo "Please enter parameter: goal + A, B, C or D
          Example: './gazebo.sh goalA'"

fi