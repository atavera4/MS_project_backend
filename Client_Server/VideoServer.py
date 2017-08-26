# Server.py

import socket
import time
import cv2
import numpy as np

cam = cv2.VideoCapture(0);
time.sleep(2)
while(True):
    ret, frame = cam.read()
    cv2.imshow('frame', frame)
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY);
    # create a socket object
    sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM);
    UDP_IP = socket.gethostname();
    UDP_port = 9999;

    d = frame.flatten();
    s = d.tostring();

    for i in xrange(20):
        sock.sendto(s[i*46080:(i+1)*46080], (UDP_IP, UDP_port));

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break;
cam.release()
cv2.destroyAllWindows();
