import bcrypt
import sqlite3
from os import remove

npassword = "12345"
password=npassword.encode('utf-8')
hashed = bcrypt.hashpw(password, bcrypt.gensalt())
connection=sqlite3.connect('main.db')
cursor=connection.cursor()
Query="CREATE TABLE USUARIOS (NOMBRE TEXT NOT NULL, APELLIDO TEXT NOT NULL,EMAIL TEXT NOT NULL UNIQUE, PASSWORD TEXT NOT NULL, CARGO TEXT, AREA TEXT, EMPRESA TEXT, ROL TEXT NOT NULL);"
cursor.execute(Query)
Query="INSERT INTO USUARIOS(NOMBRE,APELLIDO,EMAIL,PASSWORD,ROL) VALUES ('MIGUEL','AGUIRRE','miguelaguirreleon@gmail.com','%s','Administrador');" % hashed.decode('UTF-8')
cursor.execute(Query)
connection.commit()
Query="SELECT PASSWORD FROM USUARIOS WHERE EMAIL='miguelaguirreleon@gmail.com'"
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