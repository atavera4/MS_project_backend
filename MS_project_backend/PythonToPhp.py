# import json
# import urllib2

# def update_robot(angle, distance):
# 	data = {
# 	    'angle' : angle,
# 	    'distance' : distance
# 	}
# 	print("0")
# 	req = urllib2.Request('http://localhost/PHP/PythonToPhp.php')
# 	print("1")
# 	req.add_header('Content-Type', 'application/json')
# 	print("2")

# 	try:
# 		res = urllib2.urlopen(req, json.dumps(data));
# 		res.read() 
# 	except urllib2.HTTPError as error:
# 	    res = error.read()
# 	    print(res)
	    


# update_robot(1, 2);

import httplib, json
headers = { "charset" : "utf-8", "Content-Type": "application/json" }

conn = httplib.HTTPConnection("localhost")

sample = { "temp_value" : 123 }

sampleJson = json.dumps(sample, ensure_ascii = 'False')

# Send the JSON data as-is -- we don't need to URL Encode this
conn.request("POST", "/PHP/PythonToPhp.php", sampleJson, headers)

response = conn.getresponse()

print(response.read())

conn.close()