#
#
#!~/.virtualenvs/cv/bin/python
import MySQLdb
import time
import thread
import cv2
import FacialRecog
import tcpvidserv as TCP_Server

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
    def __init__(self, id, name, status, face_detect, room_attendance,fire_detect, vehicle_detect, ip_addr, device_type):
        self.id = id;
        self.name = name;
        self.status = status;
        self.face_detect = face_detect;
        self.room_attendance = room_attendance;
        self.fire_detect = fire_detect;
        self.vehicle_detect = vehicle_detect;
        self.ip_addr = ip_addr;
        self.device_type = device_type;
        return;



def LoadSqlToDeviceList(DeviceList, FacesList, event_flags):
    # load all devices and info from database.
    # this will then be scanned by each of the flags for an OFF flag.
    db = MySQLdb.connect("localhost", "root", "automationproject!", "Auto_System_Project");
    cursor = db.cursor();
    cursor.execute("SELECT * FROM Devices");
    device_query = cursor.fetchone();
    while(device_query != None):
        device_id = device_query[0];
        device_name = device_query[1];
        new_device_status = device_query[2];
        init_device_status = 'OFF';
        face_detect = device_query[3];
        room_attendance = device_query[4];
        fire_detect = device_query[5];
        vehicle_detect = device_query[6];
        device_ip_addr = device_query[7];
        device_type = device_query[8];

        # TELLS THE CHECK FUNCTIONS WHETHER IT IS BEING CALLED FOR AN INITIAL LOAD OR AN UPDATE.
        load = True;
        if(device_type == 'light'):
            device_object = Device(device_id, device_name, init_device_status,'none', 'none', 'none', 'none', device_ip_addr, device_type);
            DeviceList.append(device_object);
            CheckLight(device_object, DeviceList, event_flags, new_device_status, load);
        elif(device_type == 'camera'):
            device_object = Device(device_id, device_name, init_device_status ,face_detect,room_attendance, fire_detect, vehicle_detect, device_ip_addr, device_type);
            DeviceList.append(device_object);
            CheckCamera(device_object, DeviceList, FacesList, event_flags, new_device_status, load);
        else:
            print("Error in LoadSqlToDeviceList(): device_type does not match possible type");

        device_query = cursor.fetchone();
    db.close();
    return;


def LightControl(id, DeviceList):
    # begin new thread;
    # turn on light on gpio pins connected to ac module.
    #while(DeviceList[id].status != 'OFF'):
        #print('Light IS ON !!!');
    print(' Light Toggled !!');
    return;


def CheckLight(device, DeviceList, event_flags, init_new_status, load):
    Id = device.id;
    prev_status = '';
    updt_status = '';
    if(load):
        prev_status = device.status;
        updt_status = init_new_status;
    else:
        prev_status = DeviceList[Id].status;
        updt_status = device.status;

    # print("prev status: " + prev_status);
    # print("updt status: " + updt_status);
    if(updt_status == 'ON' and prev_status == 'OFF'):
        DeviceList[Id].status = 'ON';
        print("starting thread for Light switch with id:" + str(Id));
        thread.start_new_thread(LightControl, (Id, DeviceList, ));
    if(updt_status == 'OFF' and prev_status == 'ON'):
        print("light TURNED OFF with id: " + str(Id));
        DeviceList[Id].status = 'OFF';

    return;

def CheckCamera(device, DeviceList, FacesList, event_flags, init_new_status, load):
    Id = device.id;
    prev_status = '';
    updt_status = '';
    if(load):
        prev_status = device.status;
        updt_status = init_new_status;
    else:
        prev_status = DeviceList[Id].status;
        updt_status = device.status;

    # MAIN CAMERA ON/OFF
    if(updt_status == 'ON' and prev_status == 'OFF'):
        DeviceList[Id].status = 'ON';
        print("starting thread for camera with id:" + str(Id));
        thread.start_new_thread(FacialRecog.CameraOn, (Id, DeviceList, FacesList, event_flags, ));
    if(updt_status == 'OFF' and prev_status == 'ON'):
        DeviceList[Id].status = 'OFF';

    # FACE DETECTION ON/OFF
    if(device.face_detect == 'ON' and DeviceList[Id].face_detect == 'OFF'):
        DeviceList[Id].face_detect = 'ON';
    if(device.face_detect == 'OFF' and DeviceList[Id].face_detect == 'ON'):
        DeviceList[Id].face_detect = 'OFF';

    # ROOM/MOTION DETECTION ON/OFF
    if(device.room_attendance == 'ON' and DeviceList[Id].room_attendance == 'OFF'):
        DeviceList[Id].room_attendance = 'ON';
    if(device.room_attendance == 'OFF' and DeviceList[Id].room_attendance == 'ON'):
        DeviceList[Id].room_attendance = 'OFF';

    # FIRE DETECTION ON/OFF
        # to be added later on...

    # VEHICLE DETECTION ON/OFF
        # to be added later on .....


    return;

def AnalyzeDeviceQuery(cursor, DeviceList, FacesList, event_flags):
    #device is the SQL returned for each individual device in the form of a Tuple.
    device_query = cursor.fetchone();
    while(device_query != None):
        device_id = int(device_query[0]);
        device_name = device_query[1];
        device_status = device_query[2];
        face_detect = device_query[3];
        room_attendance = device_query[4];
        fire_detect = device_query[5];
        vehicle_detect = device_query[6];
        device_ip_addr = device_query[7];
        device_type = device_query[8];

        #

        #print("AnalyzeDeviceQuery: " + device_name + " " + device_status);
        load = False;
        if(device_type == 'light'):
            device_info = Device(device_id, device_name, device_status,'none', 'none', 'none', 'none', device_ip_addr, device_type);
            CheckLight(device_info, DeviceList, event_flags, None, load);

        elif(device_type == 'camera'):
            device_info = Device(device_id, device_name, device_status ,face_detect,room_attendance, fire_detect, vehicle_detect, device_ip_addr, device_type);
            CheckCamera(device_info, DeviceList, FacesList, event_flags, None, load);
        else:
            print("Error in AnalyzeDeviceQuery(): device_type does not match possible type");

        device_query = cursor.fetchone();
    return;



def CheckForNewFaces(FacesList, DeviceList):
    db = MySQLdb.connect("localhost", "root", "automationproject!", "Auto_System_Project");
    cursor = db.cursor();
    query_cmd = "SELECT * FROM Faces ORDER BY id DESC LIMIT 1";
    cursor.execute(query_cmd);
    # ANALYZE THE FACIAL RESULTS AND LOOK FOR THE ID OF THE LAST ADDED ENTRY.
    # curr_list_size = len(FacesList) - 1;
    # if(curr_list_size != newest_face_id-1):
    #     print("Error on CheckForNewFaces(): list size is not aligned with SQL ID");
    #     return;

    face_info = cursor.fetchone();
    if not face_info:
        print("no new face ")
        return;

    newest_face_id = str(face_info[0]);
    face_name = face_info[1];
    is_new_face = face_info[2];
    if(is_new_face == "True"):
        print("adding a new face ")
        update_cmd = "UPDATE Faces SET is_new='False' WHERE id=" + newest_face_id;
        try:
           # Execute the SQL command
           cursor.execute(update_cmd);
           # Commit your changes in the database
           db.commit();
        except:
            print("DID NOT UPDATE FACE TABLE")
           # Rollback in case there is any error
            db.rollback();

        db.close();
        # event_flags.new_face_id = newest_face_id;
        # event_flags.new_face = True;

        
        FacialRecog.RememberFace(FacesList, face_name, newest_face_id);
        new_face = Faces(face_name, int(newest_face_id));
        FacesList.append(new_face);
       
        
        
        return True;

    # event_flags.new_face = False;
    return False;


def LoadFacesFromSql(FacesList):
    FacesList.append("none"); # dummy face. to keep index in line with SQL id's

    db = MySQLdb.connect("localhost", "root", "automationproject!", "Auto_System_Project");
    cursor = db.cursor();
    cursor.execute("SELECT * FROM Faces");
    face_query = cursor.fetchone();

    while(face_query != None):
        face_id = face_query[0]
        face_name = face_query[1];
        face = Faces(face_name, int(face_id));
        FacesList.append(face)
        face_query = cursor.fetchone();
        
    db.close();
    return;


def RemoveFace():
    # work on this after everything else is done.
    # dont really need it right now.
    return;  

# CHECKS THE DB TO SEE IF USER HAS ADDED OR REMOVED A DEVICE VIA WEB UI.
def CheckDeviceAddedOrRemoved():
    ##
    return;



def main():

    print("Main program started !");

    DeviceList = [];
    event_flags = EventFlags(False, False);
    DeviceList.append("none"); # dummy device. to keep index in line with device id's
    FacesList = [];
    LoadFacesFromSql(FacesList);
    LoadSqlToDeviceList(DeviceList, FacesList, event_flags);

    # CHANGE THIS SO THAT YOU ARE ONLY LOOKING FOR A CHANGE FLAG WITH THE DEVICE ID
    # THEN JUST QUERY USING THAT ID FOR EFFICIENCY.
    while(True):

        time.sleep(1);
        CheckForNewFaces(FacesList, DeviceList);

        db = MySQLdb.connect("localhost", "root", "automationproject!", "Auto_System_Project");
        cursor = db.cursor();
        cursor.execute("SELECT * FROM Devices");
        AnalyzeDeviceQuery(cursor, DeviceList, FacesList, event_flags);
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
