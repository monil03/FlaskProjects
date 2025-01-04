from flask import Flask,render_template,request,session,redirect,url_for
from flask_socketio import SocketIO,send
import random
from string import ascii_uppercase


app=Flask(__name__)
app.config['SECRET_KEY']="abc"
socketio=SocketIO(app,cors_allowed_origins="*")


@socketio.on("connect")
def connect():
    print("connected")
   
    
@app.route("/")
def index():
    return render_template('index.html')


socketio.run(app)
