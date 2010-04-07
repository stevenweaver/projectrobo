from xml.dom.minidom import parse, parseString

class sensorData:
    def __init__(self,xml):
        self.xml = xml
        self.dom = parseString(self.xml)
        self.compass = int(self.get_data('compass'))
        self.flex = self.get_flex()
        self.us = self.get_us()
        self.beacon = int(self.get_data('beacon'))
        self.wheelencoder = self.get_data('wheelencoder')

    def update(self,xml):
        self.xml = xml
        self.dom = parseString(self.xml)
        self.compass = int(self.get_data('compass'))
        self.flex = self.get_flex()
        self.us = self.get_us()
        self.beacon = self.get_data('beacon')
        self.wheelencoder = self.get_data('wheelencoder')

    def get_data(self,text):
        return self.get_text(self.dom.getElementsByTagName(text)[0].childNodes)

    def get_flex(self):
        flex = self.dom.getElementsByTagName('flex')[0]
        left = int(self.get_text(flex.getElementsByTagName('left')[0].childNodes))       
        right= int(self.get_text(flex.getElementsByTagName('right')[0].childNodes))
        return dict(left=left,right=right)
 
    def get_us(self):
        us = self.dom.getElementsByTagName('ultrasonic')[0]
        left = int(self.get_text(us.getElementsByTagName('left')[0].childNodes)) 
        right= int(self.get_text(us.getElementsByTagName('right')[0].childNodes))
        return dict(left=left,right=right)

    def get_text(self,nodelist):
        rc = ""
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc = rc + node.data
        return rc

if __name__ == '__main__':
    # Self-testing code goes here.
    sxml= "<sensor><compass>140</compass><flex><left>500</left><right>300</right></flex><ultrasonic><left>10</left><right>10</right></ultrasonic><beacon>0</beacon><wheelencoder>???</wheelencoder></sensor>"
    sd = sensorData(sxml)
    print sd.flex['left']
    print sd.flex['right']
