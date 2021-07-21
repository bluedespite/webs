from flask import Flask,request
from flask import render_template


app = Flask(__name__)	


@app.route('/', methods=["GET","POST"])
def index():
    return render_template('index.html')

@app.route('/dashboard', methods=["GET","POST"])
def dashboard():
    if request.method=="POST":
        email=request.form.get("email")
        password=request.form.get("password")
    return 'succesfull!'+email+password

if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0')

