import cv2
import numpy as np
import os
import time
import argparse
import datetime
import imutils


## Init Face detect vars.
faceDetector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
recognizer = cv2.face.createLBPHFaceRecognizer();
font = cv2.FONT_HERSHEY_SIMPLEX;
recognizer.load("trainer/trainer.yml");

def MotionDetect():

    # construct the argument parser and parse the Arguments
    ap = argparse.ArgumentParser();
    ap.add_argument("-v", "--video", help="path to the video file");
    ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size ");
    args = vars(ap.parse_args());

    # if the video argument is None the we are reading from
    #       webcam
    if(args.get("video", None) is None):
        camera = cv2.VideoCapture(0);
        time.sleep(0.25);

    # otherwise we are reading from a video files
    else:
        camera = cv2.VideoCapture(args["video"]);

    #initialize the first frame in the video stream
    firstFrame = None;
    # init tha average frame in vid stream.
    (grabbed, frame) = camera.read();
    frame = imutils.resize(frame, width=500);
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY);
    gray = cv2.GaussianBlur(gray, (21,21), 0);
    avg = np.float32(gray);


    # loop over the frames of the video
    while(True):
        # grab the current frame and initialize
        # the occupied/unoccupied text
        (grabbed, frame) = camera.read();
        text = "Unoccupied";

        # if the frame could not be grabbed, then we have
        # reached the end of the video
        if not grabbed:
            break;

        # resize the frame, convert it to greyscale, and blur it
        frame = imutils.resize(frame, width=500);
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY);
        gray = cv2.GaussianBlur(gray, (21,21), 0);

        # if the first frame is None, initialize it
        # if (firstFrame is None):
        #     firstFrame = gray
        #     continue;

        # compute the absolute difference between the current
        # frame and the first frame/avg.
        #
        cv2.accumulateWeighted(gray, avg, 0.05); # THE 3RD ARGUMENT HERE IS TE "ALPHA". This dictates how much sudden changes affect the running average.
        #  as alpha decreases, sudden changes shows no effect on running averages.

        frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg));
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1];

        # dilate the thresholded image to fill in holes, then find
        # contours on the thresholded image.
        thresh = cv2.dilate(thresh, None, iterations=2);
        (derp,cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE);

        # loop over the contours
        for c in cnts:
            # if the contour is too small, ignore it
            if(cv2.contourArea(c) < args["min_area"]):
                continue;

            # compute the bounding box for the contour, draw it on the frame
            #   and update the text
            (x, y, w, h) = cv2.boundingRect(c);
            cv2.rectangle(frame, (x,y), (x + w, y + h), (0, 255, 0), 2);
            text = "occupied";

        # draw the text and timestamp on the frame
        cv2.putText(frame, "Room Status: {}".format(text), (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2);
        cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0,0,255), 1);

        # show the frame and record if the user presses a key
        cv2.imshow("Security Feed", frame);
        cv2.imshow("Thresh", thresh);
        cv2.imshow("frame Delta", frameDelta);
        key = cv2.waitKey(1) & 0xFF;

        # if the 'q' key is pressed, break from the loop
        if key == ord("q"):
            break;

    # clean up
    camera.release();
    cv2.destroyAllWindows();

        # process the same frame for different features sequentially
        # ex) frame_11 = Face_detect(init_frame);
        #   frame_2 = MotionDetect(frame_1);

    return;


def MotionDetect2():
    c = cv2.VideoCapture(0)
    _,f = c.read()
    f = imutils.resize(f, width=500);
    gray = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY);
    gray = cv2.GaussianBlur(gray, (21,21), 0);

    avg1 = np.float32(gray)
    avg2 = np.float32(gray)

    while(1):
        _,f = c.read()
        f = imutils.resize(f, width=500)
        gray = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21,21), 0)
        cv2.accumulateWeighted(gray,avg1,0.1)
        cv2.accumulateWeighted(gray,avg2,0.01)

        res1 = cv2.convertScaleAbs(avg1)
        res2 = cv2.convertScaleAbs(avg2)

        cv2.imshow('img',f)
        cv2.imshow('avg1',res1)
        cv2.imshow('avg2',res2)
        k = cv2.waitKey(20)

        if k == 27:
            break

    cv2.destroyAllWindows()
    c.release()
    return;

def DetectFaces2(frame):

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY);
    faces = faceDetector.detectMultiScale(gray, 1.3, 5);
    for (x,y,w,h) in faces:
        id = recognizer.predict(gray[y:y+h, x:x+w]);
        if(id == 12):
            cv2.putText(frame,'Ariel !',(x,y+h), font, 1,(255,255,255),2);
        else:
            cv2.putText(frame,'other person!',(x,y+h), font, 1,(255,255,255),2);

    return id;

MotionDetect();








#
