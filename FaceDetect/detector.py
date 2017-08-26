import cv2
import numpy as np

faceDetector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
cam = cv2.VideoCapture(0);
recognizer = cv2.face.createLBPHFaceRecognizer();
recognizer.load("trainer/trainer.yml");
id = 0;
font = cv2.FONT_HERSHEY_SIMPLEX;

def DetectFaces(camera):
    while(True):
        ret, img = cam.read();
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY);
        faces = faceDetector.detectMultiScale(gray, 1.3, 5);
        for (x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (w+x, y+h), (0,0,255), 2);
            id = recognizer.predict(gray[y:y+h, x:x+w]);
            print(id)
            if(id == 1):
                cv2.putText(img,'Ariel !',(x,y+h), font, 1,(255,255,255),2);
            elif(id == 4 or id== 2):
                cv2.putText(img,'Rock !',(x,y+h), font, 1,(255,255,255),2);
            else:
                cv2.putText(img,'other person!',(x,y+h), font, 1,(255,255,255),2);

        cv2.imshow("Face", img);
        if(cv2.waitKey(1) == ord('q')):
            break;

    cam.release();
    cv2.destroyAllWindows();
    return;


def DetectFaces2(frame):

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY);
    faces = faceDetector.detectMultiScale(gray, 1.3, 5);
    for (x,y,w,h) in faces:
        id = recognizer.predict(gray[y:y+h, x:x+w]);
        if(id == 1):
            cv2.putText(frame,'Ariel !',(x,y+h), font, 1,(255,255,255),2);
        if(id == 5):
            cv2.putText(frame,'C !',(x,y+h), font, 1,(255,255,255),2);
        else:
            cv2.putText(frame,'other person!',(x,y+h), font, 1,(255,255,255),2);

    return id;

# DetectFaces2(cam);
DetectFaces(cam);
