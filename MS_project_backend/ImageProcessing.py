import cv2
import numpy as np
import os
import time
import argparse
import datetime
import imutils
from PIL import Image
import tcpvidserv as TCP_Server
import notify
import thread

class UserData:
	def __init__(self):
		self.id;


class ImageFrame: 
	def __init__(self):
		self.img = frame;
		self.camera_id - id;
Image_Frame = ImageFrame();

class ThreadMonitor:
	def __init__(self):
		self.id = "";
		self.pointer;
		self.Add_To_Buffer_flag;
		self.Send_From_Buffer_flag;
		self.frame_buffer = [];
		self.thread_lock = thread.Lock();

	def QueueFrame(self, ):
		end_pos = len(frame_buffer) - 1;
		# THIS IS JUST A PRECAUTION UNTIL FIGURE OUT HOW PYTHON 
		# HANDLES MEMORY WITH ARRAYS.
		thread_lock.acquire();
		self.frame_buffer.append();
		thread_lock.release();

	def SendFrames(self, id, request):
		# USE A QUEUE IN HERE FIFO LIST !!!
		end_pos = len(frame_buffer) - 1;
		last
		thread_lock.acquire();

		# Send the image frame 
		request.ws_stream.send_message("my string", binary=False);
		request.ws_stream.send_message(, binary=False);

		thread_lock.release();

		return;
Thread_Handler = ThreadMonitor();




	



def web_socket_do_extra_handshake(request):
	#
	#
	pass #


def web_socket_transfer_data(request):
	# MAY NEED TO EDIT THIS IN THE STANDALONE.PY FILE TO
	# AVIOD USING GLOBAL OBJECT. ????? 

	Thread_Handler.SendFrames(request);
	
	return;



def CameraOn(request, id, DeviceList, FacesList, event_flags):
	camera_device = DeviceList[id];

	timeout_motion = time.time();

	TCP_VideoStream = TCP_Server.ConnectVidStream(camera_device, id);

	if(TCP_VideoStream is None):
		return;

	(recieved, frame) = TCP_Server.GrabFrameFromSocket(TCP_VideoStream);

	while(not recieved):
		(recieved, frame) = TCP_Server.GrabFrameFromSocket(TCP_VideoStream);
		continue;

	#MOTION DETECTION VARS INITIALIZE
	frame = imutils.resize(frame, width=500);
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY);
    gray = cv2.GaussianBlur(gray, (21,21), 0);
    avg = np.float32(gray);

    output_image = "";

    while(camera_device.status == 'ON'):
    	time.sleep(.10);
    	(recieved, frame) = TCP_Server.GrabFrameFromSocket(TCP_VideoStream);
    	if (not recieved):
    		continue;

    	text = "Unoccupied";

    	if(camera_device.room_attendance == "ON"):
    		(text, avg, frame) = MotionDetect(frame, avg, text);

    		if(camera_device.face_detect == "ON"):
    			if(text == "Occupied"):
    				frame = DetectFaces(frame, FacesList);


    		if(text == "Occupied"):
    			cnt = cv2.imencode('.png', frame)[1];
    			b64 = base64.encodestring(cnt);
    			output_image = b64;
    			


    # CLOSE THE WEB SOCKET CONNECTION
    return;



