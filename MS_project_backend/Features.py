import cv2
import numpy as np
import os
import sys
import time
import argparse
import datetime
import imutils
from PIL import Image


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
        # cv2.accumulateWeighted(gray, avg, 0.05); # THE 3RD ARGUMENT HERE IS TE "ALPHA". This dictates how much sudden changes affect the running average.
        # #  as alpha decreases, sudden changes shows no effect on running averages.

        # frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg));
        # thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1];

        # # dilate the thresholded image to fill in holes, then find
        # # contours on the thresholded image.
        # thresh = cv2.dilate(thresh, None, iterations=2);
        # (derp,cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE);

        # # loop over the contours
        # for c in cnts:
        #     # if the contour is too small, ignore it
        #     if(cv2.contourArea(c) < args["min_area"]):
        #         continue;

        #     # compute the bounding box for the contour, draw it on the frame
        #     #   and update the text
        #     (x, y, w, h) = cv2.boundingRect(c);
        #     cv2.rectangle(frame, (x,y), (x + w, y + h), (0, 255, 0), 2);
        #     text = "occupied";

        # # draw the text and timestamp on the frame
        # cv2.putText(frame, "Room Status: {}".format(text), (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2);
        # cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0,0,255), 1);

        # # add Facial recognition
        # if(text == "occupied"):
        #     DetectFaces(frame);

        # show the frame and record if the user presses a key
        cv2.imshow("Security Feed", frame);
        sys.stdout.write( frame.tostring() )
        # cv2.imshow("Thresh", thresh);
        # cv2.imshow("frame Delta", frameDelta);
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

def CheckForPerson(id, FacesList):
    if(FacesList[id].id != id):
        print("Error MISMATCH BETWEEN FacesList ID AND its index !!!")
        return;
    return FacesList[id].name;

def RememberFace(Id):
    # Generate/take sample images to train the CascadeClassifier
    # draw a box where the person will put their faces in to scan.
    # then take 20 samples and write to trainer.yml file.
    # promt the user for a name on the website.
    # use a separate DB Table to store info on the people the user adds to
    #       the system.  The main script will look here for new people by
    #           saving the last id and looking for a new one.
    #           GET THE Id from HERE (DB !!!)

    camera = cv2.VideoCapture(0); # the servers main camera
    time.sleep(0.25);
    sampleNum = 0;
    detector=cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
    while(True):
        ret, frame = camera.read();
        gray = cvtColor(frame, cv2.COLOR_BGR2GRAY);
        faces = detector.detectMultiScale(gray, 1.3, 5);
        for (x,y,w,h) in faces:
            cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2);
            # incrementing sample number
            sampleNum = sampleNum + 1;
            # Save the captured face in the dataset folder
            cv2.imwrite("dataset/User."+Id+ '.' + str(sampleNum) + ".jpg", gray[y:y+h,x:x+w]);
            cv2.imshow("frame", img);

        if(cv2.waitKey(100) & 0xFF == ord('q')):
            break;
        elif(sampleNum > 20):
            break;

    # TRAIN THE FACIAL RECOGNIZER.
    faces, Ids = getImagesAndLabels('dataSet');
    recognizer.train(faces, np.array(Ids));
    recognizer.save('trainer/trainer.yml');

    return;

def getImagesAndLabels(path):
    #get the path of all the files in the folder
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)]
    #create empth face list
    faceSamples=[]
    #create empty ID list
    Ids=[]
    #now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        #loading the image and converting it to gray scale
        pilImage=Image.open(imagePath).convert('L')
        #Now we are converting the PIL image into numpy array
        imageNp=np.array(pilImage,'uint8')
        #getting the Id from the image
        Id=int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces=detector.detectMultiScale(imageNp)
        #If a face is there then append that in the list as well as Id of it
        for (x,y,w,h) in faces:
            faceSamples.append(imageNp[y:y+h,x:x+w])
            Ids.append(Id)

    return faceSamples,Ids



def DetectFaces(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY);
    faces = faceDetector.detectMultiScale(gray, 1.3, 5);
    id = "";
    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (w+x, y+h), (0,0,255), 2);
        id = recognizer.predict(gray[y:y+h, x:x+w]);
        person = CheckForPerson(id, FacesList);
        cv2.putText(img, person, (x,y+h), font, 1,(255,255,255),2);

    return;

MotionDetect();








#
