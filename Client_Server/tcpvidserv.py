#!/usr/bin/python
import socket
import cv2
import numpy
import os
import time

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def StartStreamRecv(ip_addr):
    TCP_IP = 'localhost'
    #TCP_IP = ip_addr;
    TCP_PORT = 5006;
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    print("waiting for stream ...");
    while(True):
        s.listen(True)
        conn, addr = s.accept()
        length = recvall(conn,16)
        if(not length):
            print("not getting stream ...");
            continue;
        stringData = recvall(conn, int(length))
        data = numpy.fromstring(stringData, dtype='uint8')
        #s.close()
        decimg = cv2.imdecode(data,1)
        #decimg = data.reshape((480,640,3));
        cv2.imshow('SERVER',decimg)
        cv2.imwrite('video_frame.jpg', decimg);
        os.system('sudo cp video_frame.jpg /var/www/html/Images/video_frame.jpg');

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break;
    s.close();
    cv2.destroyAllWindows()
    return;

def ScanForDevice(ip_addr, device_type):
    TCP_IP = ip_addr;
    TCP_PORT = 5005;
    BUFFER_SIZE = 1024;
    response = '';
    while (True):
        print("Looking for Device with ip: ", ip_addr);
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((TCP_IP, TCP_PORT));
        except:
            continue;
        print("FOUND DEVICE ....");
        sock.send("Server-" + ip_addr);
        data = sock.recv(BUFFER_SIZE);
        sock.close();
        print("data recv:  ", data);
        if(data != device_type):
            print("Device type mismatch with user input vs device with this ip address ....");
            return;
        break;

    if(device_type == 'camera'):
        print("calling stream function ...");
        StartStreamRecv(ip_addr);
    else:
        ConnectLight(ip_addr);



        # length = recvall(conn,16);
        # if (not length):
        #     print("not")
        #     continue;
        # print("got client..");
        # stringData = recvall(conn, int(length));
        # if(stringData == ip_addr):
        #     print('found a device...');
            ## start streaming
            # s.close();
            # print('Calling Recv function...');
            # StartStreamRecv(ip_addr);

    return;

def AddNewDeviceConnection(ip_addr, device_type):
    ScanForDevice(ip_addr, device_type);
    return;


# connect to all on DB.
# InitDevInDatabase();
AddNewDeviceConnection("localhost", "camera");
# StartStreamRecv('localhost');
#StartCameraServer();
