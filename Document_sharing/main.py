import table 
from table import users, files
from table import db
from table import app
from flask import Flask,request,url_for,render_template,flash,redirect
from flask_login import LoginManager,login_user,logout_user,UserMixin,current_user,login_required
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import SubmitField,FileField
from flask_wtf.file import FileAllowed, FileRequired
import boto3
from botocore.exceptions import ClientError, NoCredentialsError, PartialCredentialsError
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from datetime import timedelta



s3 = boto3.client('s3',aws_access_key_id='Your-key',
    aws_secret_access_key='Your-key',
    region_name='-'
)
app.config['SECRET_KEY']="abc"
login_manager=LoginManager()
login_manager.login_view='login' # If user is not authenticated, they will be redirected here
login_manager.init_app(app) # Connects Flask-Login to your Flask app
class UploadForm(FlaskForm):
    file = FileField('Upload File', validators=[
        FileRequired(message='File is required!'),
        FileAllowed(['jpg', 'png', 'pdf', 'txt'], 'Only images, PDFs, or text files are allowed!')
    ])
    submit = SubmitField('Upload')

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=="POST":
        username=request.form.get('username')
        password=request.form.get('password')
        emailid=request.form.get('emailid')
        new_user=users(username=username,email=emailid,password=password)
        db.session.add(new_user)
        db.session.commit()  
        abc = users.query.all()
        for i in abc:
            print(i.username)
        return render_template('login.html') 
    return render_template('index.html')

@app.route('/',methods=['post','get'])
def login():
    if request.method=='POST':
        username=request.form.get('name')
        password=request.form.get('password')
        abc=users.query.filter_by(email=username).first()
        print(abc)
        if abc and abc.password==password:
            login_user(abc)
            return redirect(url_for('filesharing'))
        else:
            flash('Login Incorrect')
            return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/filesharing',methods=['post','get'])
def filesharing():
    form=UploadForm()
    file_table = files.query.filter_by(user_id=current_user.id)

    if request.method=="POST":
        file = form.file.data  # Get the file from the request
        filename = secure_filename(file.filename)
        expirationdate = datetime.today() + timedelta(days=1)
        s3.upload_fileobj(file, 'bucket-name', filename)
        url = s3.generate_presigned_url('get_object',
                                                    Params={'Bucket': 'bucket-name',
                                                            'Key': filename},
                                                    ExpiresIn=100)
        
        file_up=files(file_name=file.filename,expiration_date=expirationdate,created_at=datetime.now(),shared_link=url,user_id=current_user.id)
        
        db.session.add(file_up)
        db.session.commit()
        return redirect(url_for('filesharing'))

    return render_template('filesharing.html',form=form, ft = file_table)

@login_manager.user_loader
def loader_user(user_id):
    return table.users.query.get(user_id)

with app.app_context():
    db.create_all()

app.run(debug=True)
