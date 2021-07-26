import bcrypt
import mysql.connector
from urllib.parse import urlparse 

npassword = "12345"
password=npassword.encode('utf-8')
hashed = bcrypt.hashpw(password, bcrypt.gensalt())
f=open('database.env')
dbc = urlparse(f.read())
f.close()
connection=mysql.connector.connect(host=dbc.hostname,database=dbc.path.lstrip('/'),user=dbc.username,password=dbc.password)
cursor=connection.cursor()
Query="CREATE OR REPLACE TABLE MAIN_SENSOR.USUARIOS (ID INT NOT NULL AUTO_INCREMENT,NOMBRE TEXT NOT NULL, APELLIDO TEXT NOT NULL,EMAIL TEXT NOT NULL UNIQUE, PASSWORD TEXT NOT NULL, CARGO TEXT, AREA TEXT, EMPRESA TEXT, ROL TEXT NOT NULL,PRIMARY KEY(ID))"
cursor.execute(Query)
Query="INSERT INTO MAIN_SENSOR.USUARIOS(NOMBRE,APELLIDO,EMAIL,PASSWORD,ROL) VALUES ('MIGUEL','AGUIRRE','miguelaguirreleon@gmail.com','%s','Administrador');" % hashed.decode('UTF-8')
cursor.execute(Query)
connection.commit()
Query="SELECT PASSWORD FROM MAIN_SENSOR.USUARIOS WHERE EMAIL='miguelaguirreleon@gmail.com'"
cursor.execute(Query)
e=cursor.fetchone()
hashed1=e[0].encode('utf-8')
cursor.close()
connection.close()
# Hash a password for the first time, with a certain number of rounds
# Check that a unhashed password matches one that has previously been
#   hashed
if bcrypt.checkpw(password, hashed1):
    print("It Matches!")
else:
    print("It Does not Match :(")