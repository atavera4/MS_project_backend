#!/usr/bin/python
# -*- coding: utf-8 -*-
# This just appends a line with the word "pages" to the text file pages.txt
#with open('/var/www/txt/pages.txt', 'a') as the_file:
#	the_file.write('pages\n')
file = open("/var/www/html/test.txt", 'w');
file.write("OFF");
file.close();
