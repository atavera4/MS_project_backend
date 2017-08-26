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

def ConnectVidStream(camera_device, Id):
    ip_addr = camera_device.ip_addr;
    device_type = ScanForDevice(camera_device.ip_addr, "camera", Id);
    if(device_type is None):
        return None;
    # if(device_type == 'camera'):
    #     print("calling stream function ...");
    #     StartStreamRecv(ip_addr);
    # else:
    #     print("connecting to wifi light switch");
    #     ConnectLight(ip_addr);
    TCP_IP = camera_device.ip_addr;
    TCP_PORT = 5007;
    print("waiting for stream ...");
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1);
    sock.bind((TCP_IP, TCP_PORT));
    # GrabFrameFromSocket(sock);
    #
    # #StartStreamRecv(TCP_IP, TCP_PORT);

    return sock;

def GrabFrameFromSocket(sock):
    sock.listen(True);
    conn, addr = sock.accept();
    length = recvall(conn,16);
    if(not length):
        # print("not getting stream ...");
        return (False, None);
    #print("now getting stream !!!");
    stringData = recvall(conn, int(length));
    data = numpy.fromstring(stringData, dtype='uint8');
    decimg = cv2.imdecode(data,1)
    #decimg = data.reshape((480,640,3));

    return (True, decimg);


def ScanForDevice(ip_addr, device_type, Id):
    TCP_IP = ip_addr;
    TCP_PORT = 5005;
    timeout = time.time() + 10;# 10 seconds from now.  #60*5   # 5 minutes from now
    BUFFER_SIZE = 1024;
    response = '';
    print("Scanning for Device with id:" + str(Id));
    print("Looking for Device with ip: " + ip_addr);
    while (True):
        if(time.time() > timeout):
            print("Error: Connection Attempt to CAMERA TIMES OUT. device Id: " + str(Id));
            return None;
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.connect((TCP_IP, TCP_PORT));
        except:
            continue;
        print("FOUND DEVICE ....");
        sock.send("Server-" + ip_addr);
        data = sock.recv(BUFFER_SIZE);
        sock.close();
        print("data recv:  " + data);
        if(data != device_type):
            print("Device type mismatch with user input vs device with this ip address ....");
            return;
        break;
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

    return device_type;

def StartStreamRecv(TCP_IP, TCP_PORT):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1);
    s.bind((TCP_IP, TCP_PORT));
    while(True):
        s.listen(True)
        conn, addr = s.accept()
        length = recvall(conn,16)
        if(not length):
            print("waiting for stream ...");
            continue;
        print("now getting stream !!!");
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
    cv2.destroyAllWindows();
    return;


# def AddNewDeviceConnection(ip_addr, device_type):
#     ScanForDevice(ip_addr, device_type);
#     return;

class c:
    ip_addr = 'localhost';

a = c();
# ConnectVidStream(a, 1);
# connect to all on DB.
# InitDevInDatabase();
#AddNewDeviceConnection("localhost", "camera");
# StartStreamRecv('localhost');
#StartCameraServer();
