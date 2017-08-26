import cv2
import time

cam = cv2.VideoCapture(0);
num = 1;
while(num < 20):

    # time.sleep(1);
    ret, frame = cam.read()
    print(ret)
    cv2.imshow('frame', frame)
    num += 1;
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break;
    elif 1 == 2:
    	break;

cam.release()
cv2.destroyAllWindows()
