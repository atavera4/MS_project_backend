import os
#!/usr/bin/python
# -*- coding: utf-8 -*-
# This just appends a line with the word "open" to the text file open.txt
with open('/var/www/html/txt/open.txt', 'a') as the_file:
	the_file.write('open\n')
file = open("/var/www/html/test.txt", 'w');
file.write("ON");
file.close();

#os.system("sudo cp /var/www/html/test.txt /var/www/html/SECOND.txt");
#os.system('python /var/www/html/p4.py');
