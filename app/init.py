import bcrypt
import mysql.connector
from urllib.parse import urlparse

password = "12345"
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
f=open("database.env")
dbc = urlparse(f.read())
f.close()
connection=mysql.connector.connect (host=dbc.hostname,database=dbc.path.lstrip('/'),user=dbc.username,password=dbc.password)
cursor=connection.cursor()
Query="SHOW TABLES FROM MAIN_SENSOR"
cursor.execute(Query)
e=cursor.fetchall()
if len(e)<=0:
    Query="CREATE TABLE USUARIOS (NOMBRE TEXT NOT NULL, APELLIDO TEXT NOT NULL,EMAIL TEXT NOT NULL UNIQUE, PASSWORD TEXT NOT NULL, CARGO TEXT, AREA TEXT, EMPRESA TEXT, ROL TEXT NOT NULL);"
    cursor.execute(Query)
    Query="CREATE TABLE DISPOSITIVOS (NOMBRE TEXT NOT NULL UNIQUE, DIRECCION TEXT NOT NULL, TOKEN TEXT NOT NULL);"
    cursor.execute(Query)
    Query="INSERT INTO USUARIOS(NOMBRE,APELLIDO,EMAIL,PASSWORD,ROL) VALUES ('MIGUEL','AGUIRRE','miguelaguirreleon@gmail.com','%s','Administrador');" % hashed.decode('UTF-8')
    cursor.execute(Query)
    Query= "CREATE TABLE MAIN_SENSOR.DATA ( `ID` INT NOT NULL PRIMARY KEY AUTO_INCREMENT , `FECHA_HORA` DATETIME NOT NULL,`ID_ESTACION` TEXT NOT NULL ,`ESTACION` TEXT NOT NULL,`ID_TANQUE` TEXT NOT NULL,`TANQUE` TEXT NOT NULL,`PRODUCTO` TEXT NOT NULL,`DENSIDAD` TEXT NOT NULL,`TAG_SENSOR` TEXT NOT NULL,`DESCRIPCION` TEXT NOT NULL,`UM` TEXT NOT NULL, `RANGO_MIN` FLOAT NOT NULL, `RANGO_MAX` FLOAT NOT NULL, `TIPO` TEXT NOT NULL,`DIRECCION` TEXT NOT NULL, `MASCARA` TEXT NOT NULL, `PUERTO` TEXT NOT NULL,`ID_COMM` TEXT NOT NULL,`SERIAL` TEXT NOT NULL,`LINEAR` TEXT NOT NULL, `LATITUD` FLOAT NOT NULL,`LONGITUD` FLOAT NOT NULL,`VELOCIDAD` FLOAT NOT NULL,`MEASURE` FLOAT NOT NULL)"
    cursor.execute(Query)
    connection.commit()
    cursor.close()
    connection.close()  
