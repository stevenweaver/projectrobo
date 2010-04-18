from xml.dom.minidom import parse, parseString

class sensorData:
    def __init__(self,xml):
        self.xml = xml
        self.dom = parseString(self.xml)
        self.compass = float(self.get_data('c')) / 10 
        self.flex = self.get_flex()
        self.us = self.get_us()
        self.beacon = self.get_data('b')
        self.dis_traveled = self.get_clicks()

    def get_data(self,text):
        return self.get_text(self.dom.getElementsByTagName(text)[0].childNodes)

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

    def get_clicks(self):
        we = self.dom.getElementsByTagName('we')[0]
        a = int(self.get_text(us.getElementsByTagName('a')[0].childNodes)) 
        b = int(self.get_text(us.getElementsByTagName('b')[0].childNodes))
        return dict(left=left,right=right)

    def get_text(self,nodelist):
        rc = ""
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc = rc + node.data
        return rc

if __name__ == '__main__':
    # Self-testing code goes here.
    sxml= "<?xml version=\"1.0\"?><sensor><c>256.39</c><f><l>497</l><r>400</r></f><us><l>80</l><r>79</r></us><b>87</b><we><a>2000</a><b>1998</b></we></sensor>"
    sd = []
    sd.append(sensorData(sxml))
    sd.append(sensorData(sxml))
    print sd[0].flex['left']
    print sd[0].flex['right']
    print sd[1].flex['left']
    print sd[1].flex['right']

