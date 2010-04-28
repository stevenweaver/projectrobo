#First we need to include the new python path
import sys
#QA
DEAD_RECKON_TEST = 1
QA = 1

HOME = '/home/steven/projectrobo/code/beagleboard' 
#HOME = '/home/alkuwari/projectrobo/code/beagleboard' 
#HAPPYCAT
#HOME = '/home/steven/share/school/senior_design/projectrobo/code/beagleboard' 

#BEAGLE
#HOME = '/home/ubuntu/beagle' 
sys.path.append(HOME + '/libs/') 
sys.path.append(HOME + '/objects/') 
