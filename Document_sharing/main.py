import table 
from table import db,app
from flask import Flask,request,url_for,render_template,flash,redirect,flash
from flask_login import LoginManager,login_user,logout_user,UserMixin,current_user,login_required
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import SubmitField,FileField
from flask_wtf.file import FileAllowed, FileRequired
import boto3
from botocore.exceptions import ClientError, NoCredentialsError, PartialCredentialsError
from datetime import datetime,timedelta
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename


s3 = boto3.client('s3',aws_access_key_id='your-key',
    aws_secret_access_key='your-key',
    region_name='ap-south-1'
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
        new_user=table.users(username=username,email=emailid,password=password)
        db.session.add(new_user)
        db.session.commit()  
        abc = table.users.query.all()
        for i in abc:
            print(i.username)
        return render_template('login.html') 
    return render_template('index.html')

@app.route('/',methods=['post','get'])
def login():
    if request.method=='POST':
        username=request.form.get('name')
        password=request.form.get('password')
        abc=table.users.query.filter_by(email=username).first()
        print(abc)
        if abc and abc.password==password:
            login_user(abc)
            return redirect(url_for('filesharing'))
        else:
            flash('Login Incorrect')
            return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/filesharing',methods=['post','get'])
@login_required
def filesharing():
    form=UploadForm()
    

    if request.method=="POST":
        file = form.file.data  # Get the file from the request
        filename = secure_filename(file.filename)

        s3.upload_fileobj(file, 'aer0p1an3', filename)
        url = s3.generate_presigned_url('get_object',
                                                    Params={'Bucket': 'aer0p1an3',
                                                            'Key': filename},
                                                    ExpiresIn=60)

        abc=table.files(file_name=file.filename,shared_link=url,user_id=current_user.id)
        file_table = table.files.query.filter_by(user_id=current_user.id)

        db.session.add(abc)
        db.session.commit()




        for i in file_table:
            print(i.file_name)

        
        return render_template('filesharing.html',form=form)



    return render_template('filesharing.html',form=form)

@app.route('/show_data')
@login_required
def show_data():
    
    form=UploadForm()
    data=table.files.query.filter_by(user_id=current_user.id).all()
    current_time=datetime.now()
    print(current_time)

    return render_template('filesharing.html',data=data,form=form,current_time=current_time)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))
@login_manager.user_loader
def loader_user(user_id):
    return table.users.query.get(user_id)

@app.route('/delete/<int:id>')
def delete(id):
    abc=table.files.query.get(id)
    s3.delete_object(Bucket='aer0p1an3',Key= abc.file_name)

    db.session.delete(abc)
    db.session.commit()
    flash("Deleted Successfully")
    return redirect(url_for('filesharing'))

    
with app.app_context():
    db.create_all()

app.run(debug=True)
