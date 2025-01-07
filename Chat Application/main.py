from flask import Flask,render_template,request,session,redirect,url_for
from flask_socketio import SocketIO,send
import random
from string import ascii_uppercase


app=Flask(__name__)
app.config['SECRET_KEY']="abc"
socketio=SocketIO(app,cors_allowed_origins="*")

@app.route("/createRoom")
def createRoom():
    session.clear()
    code = ''
    for i in range(0,4):
        code += random.choice(ascii_uppercase)
    codes.append(code)  
    session['code'] = code  
    return redirect(url_for('index'))


@socketio.on("join")
def handle_join(data):
    global members
    uname = data['username']
    code = data['code']
    for room in room_details:
        if room['code'] == code:
            join_room(code)
            update_room(code)
            print(room_details)
            session['code']=code
            session['uname']=uname
            emit('message', {'msg': uname + ' has entered the room.'}, room=code)
        else:
            emit('message', {'msg': 'Invalid room code.'})
            

@socketio.on("connect")
def connect():
    print("connected")
   
    
@app.route("/")
def index():
    return render_template('index.html')


socketio.run(app)
