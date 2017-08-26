import numpy as np
import cv2
#import MySQLdb;
import time;
import pymysql


def main():

	device_status_updates = [];


	while(1):
		time.sleep(1);
		db = pymysql.connect("localhost", "website", "turtledove", "device_manager");
		cursor = db.cursor();
		cursor.execute("SELECT * FROM device_status");
		data_rows = cursor.fetchall();
		Action(data_rows);
		db.close(); 

	return;


def Action(rows):
	for row in rows:
		WhichRow(row);
		#print(row);
	return;

def WhichRow(row):
	if 1 in row:
		ControlLights(1); 
		print(row);
	return;

def ControlLights(device_id):
	#if device_id == 1:
		# insert GPIO CMD's here

	return;


main();


