import MySQLdb

# Open database connection
db = MySQLdb.connect("localhost","website","turtledove","device_manager" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
cursor.execute("SELECT VERSION()")

# Fetch a single row using fetchone() method.
while(data is not NONE):
    data = cursor.fetchone()
    print(data);

# disconnect from server
db.close()
