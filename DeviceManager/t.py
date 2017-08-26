import cv2
import time

capture = cv2.VideoCapture(0);
while(True):

    #time.sleep(1);
    ret, frame = capture.read()
    print(ret)
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break;

cam.release()
cv2.destroyAllWindows()
