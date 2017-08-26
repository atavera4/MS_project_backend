import MySQLdb;


db = MySQLdb.connect("localhost", "website", "turtledove", "device_manager");

cursor = db.cursor();

#cursor.execute("UPDATE user SET first_name='PYTHON' WHERE user_id=2;");
cursor.execute("SELECT * FROM device_status");
data = cursor.fetchone();
print(data);
data = cursor.fetchone();
print(data);


db.close();

