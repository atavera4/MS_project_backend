"""The first step is to create an SMTP object, each object is used for connection 
with one server."""

import smtplib
# server = smtplib.SMTP_SSL('smtp.googlemail.com', 465)
def Alert(msg):
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.ehlo()
	server.starttls()
	#server.ehlo()
	server.login("shadezeroat@gmail.com", "RX01Gund@mUnic0rn")
	msg = msg + "  detected";
	server.sendmail("shadezeroat@gmail.com", "atavera4@binghamton.edu", msg)
	server.quit()
	return;
# server = smtplib.SMTP('smtp.gmail.com', 587)

# #Next, log in to the server
# server.login("shadezeroat@gmail.com", "RX01Gund@mUnic0rn");

# #Send the mail
#  # The /n separates the message from the headers
# server.sendmail("shadezeroat@gmail.com", "atavera4@binghamton.edu", msg)
