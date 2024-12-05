from flask import Flask,request,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,login_user,logout_user,UserMixin

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databasename.db'
app.config["SECRET_KEY"] = "secret_key"


db=SQLAlchemy(app)
login_manager=LoginManager()
login_manager.init_app(app)

class user(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100),nullable=False)
    emailid=db.Column(db.String(100),nullable=False)
    password=db.Column(db.String(100),nullable=False)

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=="POST":
        username=request.form.get('username')
        password=request.form.get('password')
        emailid=request.form.get('emailid')
        new_user=user(username=username,emailid=emailid,password=password)
        db.session.add(new_user)
        db.session.commit()
        
        abc = user.query.all()
        for i in abc:

            print(i.username)
        
      
        return render_template('login.html')
    
    return render_template('index.html')
    
@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=='POST':
        user_name=request.form.get('name')
        password=request.form.get('password')
        abc=user.query.filter_by(emailid=user_name).first()
        print(abc.emailid)
       
        if abc.password==password:
            login_user(abc)

            return render_template('home.html',username=user_name)
    return render_template('login.html')

@login_manager.user_loader
def loader_user(user_id):
    return user.query.get(user_id)
@app.route('/')
def index():
    return render_template('index.html')

with app.app_context():
    db.create_all()
app.run(debug=True)


