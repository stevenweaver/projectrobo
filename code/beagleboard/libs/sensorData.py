from xml.dom.minidom import parse, parseString

#EXAMPLE DATA
#<sensor>
#  <gps>rawdata</gps>
#  <compass>degree</compass>
#  <flex>number</flex>
#  <ultrasonic>inches</ultrasonic>
#  <beacon>???</beacon>
#  <wheelencoder>???</wheelencoder>
#</sensor>

class sensorData:
    def __init__(self,xml):
        self.xml = xml
        self.dom = parseString(self.xml)
        self.gps = self.get_data('gps') 
        self.compass = self.get_data('compass')
        self.flex = self.get_data('flex')
        self.us = self.get_data('ultrasonic')
        self.beacon = self.get_data('beacon')
        self.wheelencoder = self.get_data('wheelencoder')

    def update(self,xml):
        self.xml = xml
        self.dom = parseString(self.xml)
        self.gps = self.get_data('gps') 
        self.compass = self.get_data('compass')
        self.flex = self.get_data('flex')
        self.us = self.get_data('ultrasonic')
        self.beacon = self.get_data('beacon')
        self.wheelencoder = self.get_data('wheelencoder')

    def get_data(self,text):
        return self.get_text(self.dom.getElementsByTagName(text)[0].childNodes)


    def get_text(self,nodelist):
        rc = ""
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc = rc + node.data
        return rc

if __name__ == '__main__':
    # Self-testing code goes here.
    sxml= "<sensor><gps>rawdata</gps><compass>degree</compass><flex>number</flex><ultrasonic>inches</ultrasonic><beacon>???</beacon><wheelencoder>???</wheelencoder></sensor>"
    sd = sensorData(sxml)
    print sd.flex
