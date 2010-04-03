from xml.dom.minidom import Document
from sensorData import *

#Data to send:
## stop, forward, reverse, left, right
#<direction>right,left,forward,reverse</direction>

class sendData:
    def createXml(self, direction):
        #<direction>right,left,forward,reverse</direction>
        doc = Document()
        dir_xml = doc.createElement("direction")
        text = doc.createTextNode(direction)
        dir_xml.appendChild(text)
        doc.appendChild(dir_xml)
        return doc.toprettyxml(indent="  ")

if __name__ == '__main__':
    # Self-testing code goes here.
    sxml= "<sensor><gps>rawdata</gps><compass>degree</compass><flex><left>number</left><right>number</right></flex><ultrasonic><left>number</left><right>number</right></ultrasonic><beacon>???</beacon><wheelencoder>???</wheelencoder></sensor>"
    sd = sensorData(sxml)
    send = sendData()
    print send.createXml("stop")
