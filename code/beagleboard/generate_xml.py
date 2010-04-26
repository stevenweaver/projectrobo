#! /bin/python

import random

f = open('./test_xml' , 'w')
com = open('./sensor_tests/log/course1', 'r')
for i in range(850):
    sxml= '<?xml version="1.0"?><sensor><c>' + com.readline().rstrip('\n') + '</c><f><l>700</l><r>700</r></f><us><l>80</l><r>80</r></us><b>' + str(((i + 5) % 180))  + '</b></sensor>\n'
    if i > 500 and i < 550: 
        #Scrape against the left hand side
        sxml= '<?xml version="1.0"?><sensor><c>' + com.readline().rstrip('\n') + '</c><f><l>' + str(random.randint(400, 500)) + '</l><r>700</r></f><us><l>80</l><r>80</r></us><b>' + str(((i + 5) % 180))  + '</b></sensor>\n'

    if i > 300 and i < 350: 
        #Scrape against the right hand side
        sxml= '<?xml version="1.0"?><sensor><c>' + com.readline().rstrip('\n') + '</c><f><l>700</l><r>' + str(random.randint(400, 500)) + '</r></f><us><l>80</l><r>80</r></us><b>' + str(((i + 5) % 180))  + '</b></sensor>\n'

    if i > 400 and i < 450: 
        #Get too close to an object
        sxml= '<?xml version="1.0"?><sensor><c>' + com.readline().rstrip('\n') + '</c><f><l>700</l><r>700</r></f><us><l>' + str(i*-1+454) + '</l><r>' + str(i*-1+454) + '</r></us><b>' + str(((i + 5) % 180))  + '</b></sensor>\n'

    #Lock on to a beacon
    if i > 700 and i < 750: 
        sxml= '<?xml version="1.0"?><sensor><c>' + com.readline().rstrip('\n') + '</c><f><l>700</l><r>700</r></f><us><l>80</l><r>80</r></us><b>' + str(random.randint(115,125))  + '</b></sensor>\n'

    print sxml
    #f.write(sxml)
