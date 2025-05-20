import ros
from your_package_name.msg import SynapticData
from std_msgs.msg import Float64
import rospy
import os

def readSynapticDataFromFile(filename):
    try:
        with open(filename, 'r') as file:
            synapticValue = float(file.readline())
        return synapticValue
    except Exception as e:
        rospy.logerr(f"Unable to open file: {filename}, Error: {str(e)}")

def synapticCallback(msg):
    synapticValue = readSynapticDataFromFile("SynapticModel.ipynb")
    motorSpeed = synapticValue

    motorPub = rospy.Publisher('/motor_speed', Float64, queue_size=1)
    motorPub.publish(motorSpeed)

def main():
    rospy.init_node('motor_control_node')

    synapticSub = rospy.Subscriber('synaptic_data', SynapticData, synapticCallback)

    rospy.spin()

if __name__ == "__main__":
    main()
