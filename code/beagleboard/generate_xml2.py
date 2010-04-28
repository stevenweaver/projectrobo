#! /bin/python

import random

sxml= "<?xml version=\"1.0\"?><motor><cl><r>1000</r><l>1000</l></cl><d><r>0</r><l>1</l></d></motor>"
#print sd[0].clicks["right"]
#print sd[0].clicks["left"]
#print sd[0].done_flags["right"]
#print sd[0].done_flags["left"]

#f = open('./test_xml' , 'w')
#com = open('./sensor_tests/log/course2', 'r')

#1182 in one foot
sxml= '<?xml version=\"1.0\"?><motor><cl><r>0</r><l>0</l></cl><d><r>1</r><l>1</l></d></motor>'
print sxml

for i in range(46):
    sxml= '<?xml version=\"1.0\"?><motor><cl><r>'+ str(520.08 * i) +'</r><l>' + str(520.08 * i) + '</l></cl><d><r>0</r><l>0</l></d></motor>'
    print sxml

sxml= '<?xml version=\"1.0\"?><motor><cl><r>0</r><l>0</l></cl><d><r>1</r><l>1</l></d></motor>'
print sxml

for i in range(5):
    sxml= '<?xml version=\"1.0\"?><motor><cl><r>'+ str(520.08 * i) +'</r><l>0</l></cl><d><r>0</r><l>0</l></d></motor>'
    print sxml

sxml= '<?xml version=\"1.0\"?><motor><cl><r>0</r><l>0</l></cl><d><r>1</r><l>1</l></d></motor>'
print sxml

for i in range(46):
    sxml= '<?xml version=\"1.0\"?><motor><cl><r>'+ str(520.08 * i) +'</r><l>' + str(520.08 * i) + '</l></cl><d><r>0</r><l>0</l></d></motor>'
    print sxml

sxml= '<?xml version=\"1.0\"?><motor><cl><r>0</r><l>0</l></cl><d><r>1</r><l>1</l></d></motor>'
print sxml

    #f.write(sxml)
