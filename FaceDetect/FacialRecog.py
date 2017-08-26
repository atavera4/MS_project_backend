import cv2
import numpy as np
import os
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


def CameraOn(id, DeviceList, event_flags):
    camera_device = DeviceList[id]; # ????
    camera = cv2.VideoCapture(0);
    time.sleep(0.25);

    # init 1st frame in the video
    first_frame = None;
    # init the average frame in vid stream.
    (grabbed, frame) = camera.read();

    # MOTION DETECTION VARS INITIALIZE.
    frame = imutils.resize(frame, width=500);
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY);
    gray = cv2.GaussianBlur(gray, (21,21), 0);
    avg = np.float32(gray);

    # loop over the frames of the video stream.
    while(camera_device.status == "ON"): # later change this to the tcp stream frames !!!
        (grabbed, frame) = camera.read();
        text = "Unoccupied";

        if(not grabbed):
            print("Error could not grabb image frame in FacialRecog.py/CameraON function !!");
            break;

        # MOTION DETECTION OPTION
        if(camera_device.room_attandeance == "ON"):
            # resize the frame, convert it to greyscale, and blur it
            frame = imutils.resize(frame, width=500);
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY);
            gray = cv2.GaussianBlur(gray, (21,21), 0);
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

        # FACIAL RECOGNITION OPTION. MOTION DETECTION MUST BE ON IN ORDER TO WORK !!
        if(camera_device.facial_recognition == "ON"):
            if(text == "Occupied"):
                DetectFaces(frame);


        # CAR DETECT AND LICENSE PLATE OPTION. MOTION MUST ALSO BE ENABLED HERE !!!
        # INSERT HERE WHEN ABLE.


        # Send Email NOTIFICATION AND UPLOAD TO GOOGLE DRIVE IF MOTION DETECTED.
        if(text == "Occupied"):
            print("uploading to google drive");
            print("sending email notification");


        # show the frame and record if the user presses a key on server for debugging only !!!!
        cv2.imshow("Security Feed", frame);
        cv2.imshow("Thresh", thresh);
        cv2.imshow("frame Delta", frameDelta);

        # write to the web server directory to display video on website.
        output_image_path = "/var/www/html/Images/video_frame" + str(id) + ".jpg";
        cv2.imwrite(output_image_path, frame);

        # if the 'q' key is pressed, break from the loop
        key = cv2.waitKey(1) & 0xFF;
        if key == ord("q"):
            break;

    # clean up
    camera.release();
    cv2.destroyAllWindows();
    return;


def RememberFace(camera, event_flags):
        event_flags.new_face = False;
        Id = event_flags.new_face_id;
        sampleNum = 0;
        camera = cv2.VideoCapture(0); # num of server camera=0.
        time.sleep(0.25);
        while(True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

                #incrementing sample number
                sampleNum=sampleNum+1
                #saving the captured face in the dataset folder
                cv2.imwrite("dataSet/User."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])

                cv2.imshow('frame',img)
            #wait for 100 miliseconds
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is morethan 20
            elif sampleNum>20:
                break;

        faces,Ids = getImagesAndLabels('dataSet')
        recognizer.train(faces, np.array(Ids))
        recognizer.save('trainer/trainer.yml')


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
        faces=faceDetector.detectMultiScale(imageNp)
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
