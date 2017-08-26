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

## Init Face detect vars.
faceDetector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml');

try:
    recognizer = cv2.face.createLBPHFaceRecognizer();
    recognizer.load("trainer/trainer.yml");
except:
    print("face data empty right now");

font = cv2.FONT_HERSHEY_SIMPLEX;


def CameraOn(id, DeviceList, FacesList, event_flags):

    camera_device = DeviceList[id]; # ????
    #camera_device = DeviceList;
    #camera_device.ip_addr = 'localhost';

    # timeout options
    timeout_motion = time.time(); #

    # RETURNS A SOCKET CONNECTION TO THE TCP WIFI CAMERA.
    TCP_VideoStream = TCP_Server.ConnectVidStream(camera_device, id);
    # camera = cv2.VideoCapture(0);
    # time.sleep(0.25);

    if(TCP_VideoStream is None):
        return;

    # init 1st frame in the video
    (recieved, frame) = TCP_Server.GrabFrameFromSocket(TCP_VideoStream);
    # (grabbed, frame) = camera.read();

    while(not recieved):
        (recieved, frame) = TCP_Server.GrabFrameFromSocket(TCP_VideoStream);
        continue;

    # MOTION DETECTION VARS INITIALIZE.
    frame = imutils.resize(frame, width=500);
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY);
    gray = cv2.GaussianBlur(gray, (21,21), 0);
    avg = np.float32(gray);


    # CHANGE THIS TO while AND THEN AN IF STATEMENT SO THAT TURNING THE CAMERA OFF WILL NOT DISCONNECT !!!!!!!!

    # loop over the frames of the video stream.
    while(camera_device.status == "ON"):
        time.sleep(.10);
        # (grabbed, frame) = camera.read();
        (recieved, frame) = TCP_Server.GrabFrameFromSocket(TCP_VideoStream);
        # if(not grabbed):
        #     print("Error could not grabb image frame in FacialRecog.py/CameraON function !!");
        #     break;
        if(not recieved):
            continue;
        #cv2.imshow('server_frame', frame);
        text = "Unoccupied";

        # MOTION DETECTION OPTION
        #print(camera_device.room_attendance);
        if(camera_device.room_attendance == "ON"): #and (time.time() > )):
            (text, avg, frame) = MotionDetect(frame, avg, text);
        #
        #print(camera_device.face_detect)
        # # FACIAL RECOGNITION OPTION. MOTION DETECTION MUST BE ON IN ORDER TO WORK !!
        if(camera_device.face_detect == "ON"):
            if(text == "Occupied"):
                frame = DetectFaces(frame, FacesList);


        # CAR DETECT AND LICENSE PLATE OPTION. MOTION MUST ALSO BE ENABLED HERE !!!
        # INSERT HERE WHEN ABLE.


        # Send Email NOTIFICATION AND UPLOAD TO GOOGLE DRIVE IF MOTION DETECTED.
	# add DB HERE WITH TABLE WITH SAME id SO js  KNOWS WHEN ROOM IS OCCUPIED.
        if(text == "Occupied"):
            # write to the web server directory to display video on website.
	    # ALSO set a timeout for the print and DB commands. 
	    # SET ANOTHER TIMER FOR EVERY 5 MIN AND WRITE A NEW IMAGE WITH A MSG THAT NO ACTIVITY SINCE DATETIME()
            output_image_path = "/var/www/html/Images/video_frame_new" + str(id) + ".jpg";
            # output_image_path = "/var/www/html/pic.jpg";
            cv2.imwrite(output_image_path, frame);
            os.system("mv "+ output_image_path + " /var/www/html/Images/video_frame" +str(id) + ".jpg" );
            # print(output_image_path)
            # print("uploading to google drive");
            # print("sending email notification");


        # show the frame and record if the user presses a key on server for debugging only !!!!
        # cv2.imshow("Security Feed", frame);
        # cv2.imshow("Thresh", thresh);
        # cv2.imshow("frame Delta", frameDelta);


        # if the 'q' key is pressed, break from the loop
        key = cv2.waitKey(1) & 0xFF;
        if key == ord("q"):
            break;

    # clean up
    #camera.release();
    cv2.destroyAllWindows();
    return;


def RememberFace(FacesList, name, id):
    # event_flags.new_face = False;
    Id = id;
    sampleNum = 0;
    camera = cv2.VideoCapture(0); # num of server camera=0.
    time.sleep(0.25);
    while(True):
        ret, img = camera.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceDetector.detectMultiScale(gray, 1.3, 5);
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2);

            #incrementing sample number
            sampleNum=sampleNum+1
            #saving the captured face in the dataset folder
            cv2.imwrite("dataSet/User."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])

            # cv2.imshow('frame',img)
        #wait for 100 miliseconds
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
        # break if the sample number is morethan 20
        elif sampleNum>20:
            break;


    recognizer_init = cv2.face.createLBPHFaceRecognizer();
    faces,Ids = getImagesAndLabels('dataSet');
    recognizer_init.train(faces, np.array(Ids));
    recognizer_init.save('trainer/trainer.yml');
    camera.release();
    print("Face Has been saved");
    # cv2.destroyAllWindows();

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

def CheckForPerson(id, FacesList):
    # print("Check for person")
    # print(id)
    index = 1; # DUMMY INDEX IS 0;

    while (index < len(FacesList)):
        if(id == FacesList[index].id):
            return FacesList[index].name
        else:
            return "OTHER"
        index+=1;


    # print(FacesList[int(id)].id)
    # if FacesList[int(id)].id != int(id):
    #     print("Error MISMATCH BETWEEN FacesList ID AND its index !!!")
    #     return;

    return "none";

def DetectFaces(img, FacesList):
    try:
        recognizer = cv2.face.createLBPHFaceRecognizer();
        recognizer.load("trainer/trainer.yml")
    except:
        print("no face data added yet")
    # print( " Detect faces")
    # print(len(FacesList))
    if(len(FacesList) == 1):
        return img;

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY);
    faces = faceDetector.detectMultiScale(gray, 1.3, 5);
    id = 0;
    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (w+x, y+h), (0,0,255), 2);
        id = recognizer.predict(gray[y:y+h, x:x+w]);
        # print(id)
        
        person = CheckForPerson(id, FacesList);
        cv2.putText(img, person, (x,y+h), font, 1,(255,255,255),2);
        # notify.Alert(person);
        # if(id == 1):
        #     cv2.putText(img,'Ariel !',(x,y+h), font, 1,(255,255,255),2);
        # elif(id == 2):
        #     cv2.putText(img,'Rock !',(x,y+h), font, 1,(255,255,255),2);
        # else:
        #     cv2.putText(img,'other person!',(x,y+h), font, 1,(255,255,255),2);
        

       
    return img;

def MotionDetect(frame, avg, text):

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
        if(cv2.contourArea(c) < 500):
            continue;

        # compute the bounding box for the contour, draw it on the frame
        #   and update the text
        (x, y, w, h) = cv2.boundingRect(c);
        cv2.rectangle(frame, (x,y), (x + w, y + h), (0, 255, 0), 2);
        text = "Occupied";

    # draw the text and timestamp on the frame
    cv2.putText(frame, "Room Status: {}".format(text), (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2);
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0,0,255), 1);
    return text, avg, frame;


def test_debug():
    class test:
        ip_addr = 'localhost';
        status = 'ON';
    class test2:
        new_face = False;
        new_face_id = 1;
        new_device = False;
    d = test();
    e = test2();
    CameraOn(2, d, e);
    return;
# test_debug();
