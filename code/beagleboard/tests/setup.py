#First we need to include the new python path
import sys
#QA
#HOME = '/home/steven/projectrobo/code/beagleboard' 
QA = 0
DEAD_RECKON_TEST = 0

#HAPPYCAT
#HOME = '/home/steven/share/school/senior_design/projectrobo/code/beagleboard' 

#BEAGLE
HOME = '/home/ubuntu/beagle' 
sys.path.append(HOME + '/libs/') 
sys.path.append(HOME + '/objects/') 
