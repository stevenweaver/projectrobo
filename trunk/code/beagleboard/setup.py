#First we need to include the new python path
import sys
#QA
HOME = '/home/steven/projectrobo/code/beagleboard' 
QA = 1
#HAPPYCAT
#HOME = '/home/steven/share/school/senior_design/projectrobo/code/beagleboard' 

#BEAGLE
#HOME = '/home/ubuntu/beagle' 
sys.path.append(HOME + '/libs/') 
sys.path.append(HOME + '/objects/') 
