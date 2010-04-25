#! /bin/python

import random

f = open('./test_xml' , 'w')
com = open('./sensor_tests/log/course1', 'r')
for i in range(850):
    sxml= '<?xml version="1.0"?><sensor><c>' + com.readline().rstrip('\n') + '</c><f><l>' + str(random.randint(300, 700)) + '</l><r>' + str(random.randint(300, 700)) + '</r></f><us><l>' + str(random.randint(0,10)) + '</l><r>' + str(random.randint(0,10))  + '</r></us><b>' + str(random.randint(0,180))  + '</b><we><a>' + str(random.randint(0,10000))  + '</a><b>' + str(random.randint(0,10000))  + '</b></we></sensor>\n'
    print sxml
    #f.write(sxml)
