from xml.dom.minidom import parse, parseString
import math

class sensorData:
    def __init__(self,xml):
        self.xml = xml
        self.dom = parseString(self.xml)
        self.compass = self.get_compass() 
        self.flex = self.get_flex()
        self.us = self.get_us()
        self.beacon = self.get_data('b')

    def get_data(self,text):
        return self.get_text(self.dom.getElementsByTagName(text)[0].childNodes)

    def get_compass(self):
        #compass = float(self.get_data('c')) / 10 
        compass = float(self.get_data('c')) 

        #compass convert according to http://code.google.com/p/projectrobo/wiki/Compass_Characterization
        #Within ~5 degrees of error
        if compass < 150:
            degrees = (compass * 9./5)

        #Found this equation using a logorithmic best line curve: y = 99.415*ln(x) - 223.49  
        #Within ~7 degrees of error
        else:
            degrees = 99.415*math.log(compass) - 223.49 

        return degrees            
         
    def get_flex(self):
        flex = self.dom.getElementsByTagName('f')[0]
        left = int(self.get_text(flex.getElementsByTagName('l')[0].childNodes))       
        right= int(self.get_text(flex.getElementsByTagName('r')[0].childNodes))
        return dict(left=left,right=right)
 
    def get_us(self):
        us = self.dom.getElementsByTagName('us')[0]
        left = int(self.get_text(us.getElementsByTagName('l')[0].childNodes)) 
        right= int(self.get_text(us.getElementsByTagName('r')[0].childNodes))
        return dict(left=left,right=right)

    def get_text(self,nodelist):
        rc = ""
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc = rc + node.data
        return rc

if __name__ == '__main__':
    # Self-testing code goes here.
    sxml= "<?xml version=\"1.0\"?><sensor><c>2563.9</c><f><l>497</l><r>400</r></f><us><l>80</l><r>79</r></us><b>87</b></sensor>"
    sd = []
    sd.append(sensorData(sxml))
    sd.append(sensorData(sxml))
    print sd[0].compass
