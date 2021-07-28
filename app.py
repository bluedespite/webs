from flask import Flask,request,redirect,url_for
import json
from flask import render_template,session
import sqlite3
import json
import secrets
import bcrypt
import init


app = Flask(__name__)	
app.secret_key = secrets.token_urlsafe(20)

user={ 'email':'','password':'','nombre':'','apellido':'','cargo':'','area':'','empresa':'','rol':''}

def validar_usuario(user):
    connection=sqlite3.connect('main.db')
    cursor=connection.cursor()
    Query="SELECT PASSWORD FROM `USUARIOS` WHERE email='%(email)s' " % user
    cursor.execute(Query)
    e=cursor.fetchone()
    cursor.close()
    connection.close()    
    try:
        hashed=e[0].encode('utf-8')
        return bcrypt.checkpw(user['password'].encode('utf-8'), hashed)
    except:
        return False

def check_usuario(user):
    connection=sqlite3.connect('main.db')
    cursor=connection.cursor()
    Query="SELECT PASSWORD FROM `USUARIOS` WHERE email='%(email)s' " % user
    cursor.execute(Query)
    e=cursor.fetchone()
    try:
        if len(e[0])>0:
            return True
        else:
            return False
    except:
        return False

def save_usuario(user):
    connection=sqlite3.connect('main.db')
    cursor=connection.cursor()
    password = user['password'].encode('utf-8')
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    user['hashed'] = hashed.decode('UTF-8')
    Query="INSERT INTO MAIN_SENSOR.USUARIOS(NOMBRE,APELLIDO,EMAIL,PASSWORD,CARGO, AREA, ROL,EMPRESA) VALUES ('%(nombre)s','%(apellido)s','%(email)s','%(hashed)s','%(cargo)s','%(area)s','%(rol)s','%(empresa)s')" %  user
    print(Query)
    cursor.execute(Query)
    connection.commit()
    cursor.close()
    connection.close()
    message = {
            'status': 200,
            'message': 'OK',
            'data': 'Se insertó registro'
        }
    resp =  json.dumps(message, indent=4)
    return resp

def update_usuario(user):
    connection=sqlite3.connect('main.db')
    cursor=connection.cursor()
    password = user['npassword'].encode('utf-8')
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    user['hashed'] = hashed.decode('UTF-8')
    print(hashed)
    print(user['hashed'])
    Query="UPDATE USUARIOS SET NOMBRE = '%(nombre)s', APELLIDO = '%(apellido)s' , CARGO = '%(cargo)s', PASSWORD = '%(hashed)s', AREA = '%(area)s', EMPRESA = '%(empresa)s', ROL = '%(rol)s' WHERE EMAIL = '%(email)s' " % user
    cursor.execute(Query)
    connection.commit()
    cursor.close()
    connection.close()
    message = {
            'status': 200,
            'message': 'OK',
            'data': 'Se actualizó Registro'
        }
    resp =  json.dumps(message, indent=4)
    return resp

def get_usuario(email):
    connection=sqlite3.connect('main.db')
    cursor=connection.cursor()
    Query="SELECT * FROM `USUARIOS` WHERE email='%s' " % email
    cursor.execute(Query)
    data=cursor.fetchone()
    cursor.close()
    connection.close()
    user={}    
    user['nombre']=data[0]
    user['apellido']=data[1]
    user['email']=data[2]
    user['cargo']=data[4]
    user['area']=data[5]
    user['empresa']=data[6]
    user['rol']=data[7]
    user['password']=""
    message = {
        'status': 200,
        'message': 'OK',
        'data': user
    }
    resp =  json.dumps(message, indent=4)
    return resp

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
            user={}
            user['email']=request.form.get("email")
            user['password']=request.form.get("password")
            if validar_usuario(user):
                session['username']=user['email']
                user = {}
                return render_template('dashboard.html')
            else:
                return redirect(url_for('index'))
        else:
                return redirect(url_for('index'))

@app.route('/usuarios')
def usuarios():
    user={ 'email':'','password':'','nombre':'','apellido':'','cargo':'','area':'','empresa':'','rol':''}
    if 'username' in session:
        if request.method=="POST":
            email=request.form.get("email")
            user=get_usuario(email)
            return render_template('usuarios.html', user=user)
        else:
            return render_template('usuarios.html',user=user)
    else:
        return redirect(url_for('index'))

@app.route('/get_user', methods=["GET","POST"])
def get_user():
    if 'username' in session:
        if request.method=="POST":
            email=request.form.get("email")
            return get_usuario(email)
        else:
            message = {
                'status': 404,
                'message': 'FAIL',
                'data': 0
            }
            return json.dumps(message, indent=4)
    else:
        message = {
            'status': 404,
            'message': 'No permitido',
            'data': 0
        }
        return json.dumps(message, indent=4)


@app.route('/save_user', methods=["GET","POST"])
def save_user():
    if 'username' in session:
        if request.method=="POST":
            user['nombre']=request.form.get("nombre")
            user['apellido']=request.form.get("apellido")
            user['cargo']=request.form.get("cargo")
            user['rol']=request.form.get("rol")
            user['area']=request.form.get("area")
            user['empresa']=request.form.get("empresa")
            user['email']=request.form.get("email")
            user['password']=request.form.get("password")
            user['npassword']=request.form.get("npassword")
            if check_usuario(user):
                return update_usuario(user)
            else:
                return save_usuario(user)
        else:
            message = {
                'status': 404,
                'message': 'FAIL',
                'data': 'Actualizacion Fallida'
            }
            return json.dumps(message, indent=4)
    else:
        message = {
            'status': 404,
            'message': 'No permitido',
            'data': 0
        }
        return json.dumps(message, indent=4)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('index.html')

if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0')
