source devel/setup.bash

TEST=$1

if [ "$TEST" != "" ]; then
    a='TEST'
    b=$1
    c="${a} ${b}"
    echo "${c}"
fi

if [ "$TEST" == "A" ]; then
   
   roslaunch perception testA.launch

elif [ "$TEST" == 'B' ]; then
    roslaunch perception testB.launch

elif [ "$TEST" == "C" ]; then
    roslaunch perception testC.launch

elif [ "$TEST" == "D" ]; then
    roslaunch perception testD.launch

else 
    echo "Please enter parameter: A, B, C or D
          Example: './gazebo.sh A'"

fi