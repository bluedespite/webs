from flask import Flask,request,redirect,url_for
import json
from flask import render_template,session
import mysql.connector
from urllib.parse import urlparse 
import json
import pandas as pd
import secrets

#CREATE TABLE MAIN_SENSOR.USUARIOS (ID INT NOT NULL AUTO_INCREMENT,NOMBRE TEXT NOT NULL, APELLIDO TEXT NOT NULL,EMAIL TEXT NOT NULL, PASSWORD TEXT NOT NULL, CARGO TEXT, AREA TEXT, EMPRESA TEXT, ROL TEXT NOT NULL,PRIMARY KEY(ID));
#INSERT INTO MAIN_SENSOR.USUARIOS(NOMBRE,APELLIDO,EMAIL,PASSWORD,ROL) VALUES ('MIGUEL','AGUIRRE','miguelaguirreleon@gmail.com',MD5('12345'),'ADMINISTRADOR');

user={}
user['email']=""
user['password']=""
user['nombre']=""
user['apellido']=""
user['cargo']=""
user['area']=""
user['empresa']=""
user['rol']=""

def validar_usuario(user):
    f=open('database.env')
    dbc = urlparse(f.read())
    f.close()
    connection=mysql.connector.connect(host=dbc.hostname,database=dbc.path.lstrip('/'),user=dbc.username,password=dbc.password)
    cursor=connection.cursor()
    Query="SELECT * FROM `USUARIOS` WHERE email=%(email)s AND password=MD5(%(password)s)"
    cursor.execute(Query,user)
    c=len(cursor.fetchall())
    cursor.close()
    connection.close()
    if c>0 :
        return True
    else:
        return False

def usuario(email):
    f=open('database.env')
    dbc = urlparse(f.read())
    f.close()
    connection=mysql.connector.connect(host=dbc.hostname,database=dbc.path.lstrip('/'),user=dbc.username,password=dbc.password)
    cursor=connection.cursor()
    Query="SELECT * FROM `USUARIOS` WHERE email='%s' ORDER BY ID DESC LIMIT 1" % email
    cursor.execute(Query)
    usuarios=cursor.fetchall()
    cursor.close()
    connection.close()
    user={}    
    user['email']=""
    user['password']=""
    user['nombre']=""
    user['apellido']=""
    user['cargo']=""
    user['area']=""
    user['empresa']=""
    user['rol']=""
    for data in usuarios:
        user['nombre']=data[1]
        user['apellido']=data[2]
        user['email']=data[3]
        user['password']=data[4]
        user['cargo']=data[5]
        user['area']=data[6]
        user['empresa']=data[7]
        user['rol']=data[8]
    message = {
            'status': 200,
            'message': 'OK',
            'data': user
        }
    resp =  json.dumps(message, indent=4)
    return resp


app = Flask(__name__)	
app.secret_key = secrets.token_urlsafe(20)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/dashboard', methods=["GET","POST"])
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html')
    else:
        if request.method=="POST":
            print("ok")
            user['email']=request.form.get("email")
            user['password']=request.form.get("password")
            if validar_usuario(user):
                session['username']=user['email']
                user['email']=""
                user['password']=""
                return render_template('dashboard.html')
            else:
                return redirect(url_for('index'))
        else:
                return redirect(url_for('index'))

@app.route('/usuarios')
def usuarios():
    if 'username' in session:
        return render_template('usuarios.html', user=user)
    else:
        return redirect(url_for('index'))

@app.route('/get_user', methods=["GET","POST"])
def get_user():
    if request.method=="POST":
        email=request.form.get("email")
        print(email)
        return usuario(email)
    else:
        message = {
            'status': 404,
            'message': 'FAIL',
            'data': 0
        }
        resp =  json.dumps(message, indent=4)
        return resp
@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('index.html')

if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0')
