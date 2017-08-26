       #!/usr/bin/python
import socket
import cv2
import numpy
import time



capture = cv2.VideoCapture(0)

# MAYBE USE MULTICAST ??????????
# Server will use the ip from user input database to locate this client.
def MakeVisibleToServer():
    # HOST A SERVER AND WAIT FOR THE MAIN SERVER
    #   TO FIND THIS CLIENT.
    TCP_IP = 'localhost';
    TCP_PORT = 5005;
    BUFFER_SIZE = 1024;

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    s.bind((TCP_IP, TCP_PORT));
    print("waiting to be found ...");
    s.listen(True);
    conn, addr = s.accept();

    while(True):
        data = conn.recv(BUFFER_SIZE);
        if not data:
            break;
        print("Server has found me ...", data);
        # PARSE THE MESSAGE So that the 1st half is name and second is ip
        # confirm its server. then take its ip and connect.
        info = data.split('-');
        if(info[0] == "Server"):
            server_ip_addr = info[1];
            #ConnectToServer(server_ip_addr);
            conn.send("camera");
            conn.close();
            print("ip is ", server_ip_addr);
            time.sleep(2);
            StartStreamSend(server_ip_addr);
            break;
    return;

def ConnectToServer(server_ip_addr):
    # THIS IS TOO KEEP CHECKING FOR THE SERVER TO BE TURNED ON!!
    while (True):
        print("waiting for server .....");
        try:
            sock = socket.socket()
            sock.connect((TCP_IP, TCP_PORT))
        except:
            continue;
        print('Server is Up and Running');
        ## send this devices ip_addr.
        ip_addr = 'localhost';
        #sock.send(str(len(ip_addr)).ljust(16));
        sock.send(ip_addr);
        data = sock.recv(BUFFER_SIZE);
        print(data);
        sock.close();
        ## wait for 2 seconds until server is ready.
        #time.sleep(2000);
        print('calling stream function');
        #StartStreamSend(ip_addr);
        break;

    return;

def StartStreamSend(ip_addr):
    TCP_IP = ip_addr; #'localhost'; # IP OF Server
    TCP_PORT = 5006;
    BUFFER_SIZE = 1024;
    while(True):
        print("waiting for server .....")
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
            sock.connect((TCP_IP, TCP_PORT));
        except:
            continue;
        break;

    print("starting video stream ......");
    while(True):
        ret, frame = capture.read();
        cv2.imshow('frame', frame);
        sock = socket.socket();
        sock.connect((ip_addr, TCP_PORT));
        encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90];
        result, imgencode = cv2.imencode('.jpg', frame, encode_param);
        data = numpy.array(imgencode);
        stringData = data.tostring();
        sock.send( str(len(stringData)).ljust(16));
        sock.send(stringData);
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break;
    sock.close();
    capture.release();
    cv2.destroyAllWindows();

    return;

MakeVisibleToServer();
# StartStreamSend('localhost');
# while(True):
#     ret, frame = capture.read()
#     cv2.imshow('frame', frame)
#     sock = socket.socket()
#     sock.connect((TCP_IP, TCP_PORT))
#
#
#     encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
#     result, imgencode = cv2.imencode('.jpg', frame, encode_param)
#     data = numpy.array(imgencode)
#     stringData = data.tostring()
#
#     sock.send( str(len(stringData)).ljust(16));
#     sock.send( stringData );
#     #sock.close()
#
#     #decimg=cv2.imdecode(data,1)
#     #cv2.imshow('CLIENT',decimg)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break;
# sock.close();
# cam.release()
# cv2.destroyAllWindows()
