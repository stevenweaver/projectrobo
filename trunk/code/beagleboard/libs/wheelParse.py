from xml.dom.minidom import parse, parseString

#<?xml version=\"1.0\"?><motor><cl><r>%d<r><l>%d</l><cl><d><r>%d</r><l>%d</l></d></motor>
TICKS_TO_FOOT = 1182

class wheelParse:
    def __init__(self,xml):
        self.xml = xml
        self.dom = parseString(self.xml)
        self.ft = self.get_clicks() 
        self.done_flags = self.get_done_flags()

    def get_data(self,text):
        return self.get_text(self.dom.getElementsByTagName(text)[0].childNodes)

    def get_clicks(self):
        clicks = self.dom.getElementsByTagName('cl')[0]
        left = float(self.get_text(clicks.getElementsByTagName('l')[0].childNodes))/TICKS_TO_FOOT       
        right= float(self.get_text(clicks.getElementsByTagName('r')[0].childNodes))/TICKS_TO_FOOT
        return dict(left=left,right=right)
 
    def get_done_flags(self):
        done_flag = self.dom.getElementsByTagName('d')[0]
        left = int(self.get_text(done_flag.getElementsByTagName('l')[0].childNodes)) 
        right= int(self.get_text(done_flag.getElementsByTagName('r')[0].childNodes))
        return dict(left=left,right=right)

    def get_text(self,nodelist):
        rc = ""
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc = rc + node.data
        return rc

if __name__ == '__main__':
    # Self-testing code goes here.
    sxml= "<?xml version=\"1.0\"?><motor><cl><r>1000</r><l>1000</l></cl><d><r>0</r><l>1</l></d></motor>"
    sd = []
    sd.append(wheelParse(sxml))
    sd.append(wheelParse(sxml))
    print sd[0].ft["right"]
    print sd[0].ft["left"]
    print sd[0].done_flags["right"]
    print sd[0].done_flags["left"]
