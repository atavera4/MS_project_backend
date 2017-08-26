#
#
#!~/.virtualenvs/cv/bin/python
import MySQLdb
import time
import thread
import cv2
import FacialRecog
import tcpvidserv as TCP_Server
import tcpvidclient as TCP_Client

# Class to store the device flags from SQL DB.
class Faces:
    def __init__(self, name, id):
        self.name = name;
        self.id = id;
        return;

class EventFlags:
    def __init__(self, new_face, new_device):
        self.new_face = new_face;
        self.new_face_id = 0;
        self.new_device = new_device;
        return;

class Device:
    # CREATE an array of device objects.
    def __init__(self, name, id, status, ip_addr):
        self.id = id;
        self.name = name;
        self.status = status;
        self.face_detect = face_detect;
        self.room_attandeance = room_attandeance;
        self.fire_detect = fire_detect;
        self.vehicle_detect = vehicle_detect;
        self.ip_addr = ip_addr;
        self.device_type = device_type;
        return;



def LoadSqlToDeviceList(DeviceList, event_flags):
    # load all devices and info from database.
    # this will then be scanned by each of the flags for an OFF flag.
    db = MySQLdb.connect("localhost", "Devices", "automationproject!", "Auto_System_Project");
    cursor = db.cursor();
    cursor.execute("SELECT * FROM Devices");
    device = cursor.fetchone();
    while(device != None):
        device_id = device[0];
        device_name = device[1];
        device_status = device[2];
        face_detect = device[3];
        room_attendance = device[4];
        fire_detect = device[5];
        vehicle_detect = device[6];
        device_ip_addr = device[7];
        device_type = device[8];

        if(device_type == 'light'):
            device = Device(device_id, device_name, device_status,
            'none', 'none', 'none', 'none', device_ip_addr, device_type);
            DeviceList.append(device);
            CheckLight(device, DeviceList, event_flags);
        else:
            device = Device(device_id, device_name, device_status ,face_detect,
            room_attendance, fire_detect, vehicle_detect, device_ip_addr, device_type);
            DeviceList.append(device);
            CheckCamera(device, DeviceList, event_flags);

        TCP_Server.AddNewDeviceConnection(ip_addr, device_type);
        device = cursor.fetchone();

    return;


def LightControl(id, DeviceList):
    # begin new thread;
    # turn on light on gpio pins connected to ac module.
    while(DeviceList[id].status != 'OFF'):
        print('Light IS ON !!!');
    print(' Light DONE !!');
    return;

def CameraControl(id, DeviceList):

    # capture = cv2.VideoCapture(0);
    # while(DeviceList[id].status != 'OFF'):
    #     ret, frame = capture.read()
    #     cv2.imshow('frame', frame)
    #     print('HERE !!!!');
    #     # write frame to server directory
    #     #cv2.imwrite(frame, '/var/www/html/images/video_frame.jpg');
    #
    # cam.release();
    # cv2.destroyAllWindows();
    print("ON ON ON?")
    capture = cv2.VideoCapture(0);
    while(DeviceList[id].status != 'OFF'):
        if(DeviceList[id].id != id):
            print("Error mismatch with device id and its index in Camera control func !!");
            return;
        camera_device = DeviceList[id];
        FacialRecog.CameraOn(camera_device);

        else:
            time.sleep(.05);
            ret, frame = capture.read()
            #print(ret)
            #cv2.imshow('frame', frame)
            cv2.imwrite('/var/www/html/Images/video_frame.jpg', frame);
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break;

                # fix the js and php.
                # then make the detect func retrun the frame to display it.

    capture.release()
    cv2.destroyAllWindows()


    return;

def CheckLight(device, DeviceList, event_flags):
    Id = device.id;
    if(device.status == 'ON' and DeviceList[Id].status == 'OFF'):
        DeviceList[Id].status = 'ON';
        thread.start_new_thread(LightControl, (Id, DeviceList, ));
    if(device.status == 'OFF'):
        DeviceList[device_id].status = 'OFF';

    return;

def CheckCamera(device, DeviceList, event_flags):
    Id = device.id;
    new_status = device.status;
    current_status = DeviceList[device.id].status;
    # MAIN CAMERA ON/OFF
    if(device.status == 'ON' and DeviceList[Id].status == 'OFF'):
        DeviceList[Id].status = 'ON';
        thread.start_new_thread(FacialRecog.CameraOn, (Id, DeviceList, event_flags, ));
    if(device.status == 'OFF' and DeviceList[Id].status == 'ON'):
        DeviceList[Id].status = 'OFF';

    # FACE DETECTION ON/OFF
    if(device.face_detect == 'ON' and DeviceList[Id].face_detect == 'OFF'):
        DeviceList[device_id].status = 'ON';
    if(device.face_detect == 'OFF' and DeviceList[Id].face_detect == 'ON'):
        DeviceList[Id].face_detect = 'OFF';

    # ROOM/MOTION DETECTION ON/OFF
    if(device.room_attendance == 'ON' and DeviceList[Id].room_attendance == 'OFF'):
        DeviceList[Id].room_attendance = 'ON';
    if(device.room_attendance == 'ON') and DeviceList[Id].room_attendance == 'OFF'):
        DeviceList[Id].room_attendance = 'OFF';

    # FIRE DETECTION ON/OFF
        # to be added later on...

    # VEHICLE DETECTION ON/OFF
        # to be added later on .....


    return;

def AnalyzeDeviceQuery(cursor, DeviceList, event_flags):
    #device is the SQL returned for each individual device in the form of a Tuple.
    device = cursor.fetchone();
    while(device != None):
        device_id = device[0];
        device_name = device[1];
        device_status = device[2];
        face_detect = device[3];
        room_attendance = device[4];
        fire_detect = device[5];
        vehicle_detect = device[6];
        device_ip_addr = device[7];
        device_type = device[8];

        if(device_type == 'light'):
            device = Device(device_id, device_name, device_status,
            'none', 'none', 'none', 'none', device_ip_addr, device_type);
            CheckLight(device_info, DeviceList, event_flags);

        elif(device_type == 'camera'):
            device_info = Device(device_id, device_name, device_status ,face_detect,
            room_attendance, fire_detect, vehicle_detect, device_ip_addr, device_type);
            CheckCamera(device_info, DeviceList, event_flags);

        current_device = cursor.fetchone();
    return;


def CheckForNewFaces(FacesList, DeviceList):
    db = MySQLdb.connect("localhost", "root", "automationproject!", "Auto_System_Project");
    cursor = db.cursor();
    query_cmd = "SELECT * FROM Faces ORDER BY id DESC LIMIT 1";
    cursor.execute(query_cmd);
    # ANALYZE THE FACIAL RESULTS AND LOOK FOR THE ID OF THE LAST ADDED ENTRY.
    last_face = FacesList[FacesList.size()].id;
    face_info = cursor.fetchone();
    newest_face_id = face_info[0];
    face_name = face_info[1];
    is_new_face = face_info[2];
    if(is_new_face == "TRUE"):
        update_cmd = "UPDATE FACES SET new='FALSE' WHERE id=" + newest_face_id;
        try:
           # Execute the SQL command
           cursor.execute(update_cmd);
           # Commit your changes in the database
           db.commit();
        except:
           # Rollback in case there is any error
           db.rollback();

        db.close();
        # event_flags.new_face_id = newest_face_id;
        # event_flags.new_face = True;

        # add new face here.
        # this does not need to go in any of the CameraON threads
        #  b/c it will use the camera mounted on the server and not
        #  any of the remote TCP camera nodes which is what the threads are for.
        FacialRecog.RememberFace(face_name);
        return True;

    # event_flags.new_face = False;
    return False;

def RemoveFace():
    # work on this after everything else is done.
    # dont really need it right now.
    return;

def main():
    print("Main program started !");
    DeviceList = [];
    event_flags = EventFlags(False, False);
    DeviceList.append("none"); # dummy device. to keep index in line with device id's
    FacesList = [];
    LoadSqlToDeviceList(DeviceList);

    # CHANGE THIS SO THAT YOU ARE ONLY LOOKING FOR A CHANGE FLAG WITH THE DEVICE ID
    # THEN JUST QUERY USING THAT ID FOR EFFICIENCY.
    while(True):

        time.sleep(1);
        CheckForNewFaces(FacesList, DeviceList);


        db = MySQLdb.connect("localhost", "root", "automationproject!", "Auto_System_Project");
        cursor = db.cursor();
        cursor.execute("SELECT * FROM DEVICES");
        AnalyzeDeviceQuery(cursor, DeviceList, event_flags);
        # NOW ADD THE FACES TABLE !!!!! User pushes a button and the imshow 
        # appears on server cameras.


    db.close();
    return;

main();


# TEST THIS AND THEN DO THE TCP VIDEO STUFF FOR CameraON function !!!!!
# add the facial rec PHP file and JS function fo its submit button.
#improve UI
# add more features.



# # open database connection
# db = MySQLdb.connect("localhost", "project", "pass", "Web_Page");
#
# # prepare a cursor object using cursor() method
# cursor = db.cursor();
#
# # execute SQL query using execute() method.
# cursor.execute("SELECT status FROM DEVICES");
#
# #FETCH a single row using fetchone() method.
# data = cursor.fetchone();
# # while(data is not None):
# #     print(data);
# #     data = cursor.fetchone()
#
# if('ON' in data):
#     print("got it!!");
#     print(data);
#
# cursor.execute("SELECT function FROM DEVICES");
# print(cursor.fetchone());
# # disconnect from server.
# db.close();
