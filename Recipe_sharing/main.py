import table 
from table import db,app,post_receipe,users,comments,likes
from flask import Flask,request,url_for,render_template,flash,redirect,flash,send_file
from flask_login import LoginManager,login_user,logout_user,UserMixin,current_user,login_required
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,FileField,IntegerField
from wtforms.validators import DataRequired
from flask_wtf.file import FileRequired,FileAllowed
import io 

app.config['SECRET_KEY']="abc123"
login_manager=LoginManager()
login_manager.login_view='login' # If user is not authenticated, they will be redirected here
login_manager.init_app(app) # Connects Flask-Login to your Flask app


class addPosts(FlaskForm):
    PT=StringField('Post Title',validators=[DataRequired()])
    PD=StringField('Post Description',validators=[DataRequired()])
    image=FileField("Image",validators=[FileRequired(message="This file is required"),FileAllowed(['jpg','png'],'Only Images are Allowed')])
    submit = SubmitField("Submit")

@app.route('/signup',methods=['GET','POST'])
def signup():
    flag=False
    if request.method=="POST":
        username=request.form.get('username')
        password=request.form.get('password')
        emailid=request.form.get('emailid')
        
        for us in users.query.all():
            if us.username==username or us.email==emailid:
                flag=True
        if not flag:
            new_user=users(username=username,email=emailid,password=password)
            db.session.add(new_user)
            db.session.commit()  
            return render_template('login.html')
        else:
            flash("Username/Emaild ID already exists!")
            return redirect(url_for('signup'))
            
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
            return redirect(url_for('addPost'))
        else:
            flash('Login Incorrect')
            return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/add_post',methods=['POST','GET'])
@login_required
def addPost():
    form=addPosts()
    abc=post_receipe.query.all()

    if form.validate_on_submit():
        print('hiiiii')
        pt=form.PT.data
        pd=form.PD.data
        image=form.image.data
        addpost=post_receipe(post_title=pt,post_description=pd,image=image.read(),user_id=current_user.id)
        db.session.add(addpost)
        db.session.commit()
        return redirect(url_for('addPost'))
    return render_template('post_receipe.html',form=form,data=abc)

@app.route('/image/<int:id>')
def imageProcess(id):
    user = post_receipe.query.get(id)  # Retrieve user by ID
    if user and user.image:
        return send_file(
            io.BytesIO(user.image),  # Convert binary data to a file-like object
            mimetype='image/jpeg',  # MIME type (e.g., 'image/png' for PNG images)
            as_attachment=False,    # Don't trigger download
        )
    return "Image not found", 404

@login_manager.user_loader
def loader_user(user_id):
    return users.query.get(user_id)

@app.route('/get_receipe/<int:id>')
def getReceipe(id):
    all_comments = comments.query.filter_by(post_id=id).all()
    getData=post_receipe.query.get(id)
    post_likes = post_receipe.query.get(id)
    return render_template('getData.html',data=getData, all_comments = all_comments,likes=post_likes.likes)

@app.route('/add_comment/<int:id>',methods=['POST','GET'])
def addComment(id):

    if request.method=="POST":
        user_comment = request.form.get('comment')
        new_comment = comments(user_id = current_user.id, post_id = id, comment = user_comment, user_name = current_user.username)
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('getReceipe',id=id))
    return redirect(url_for('getReceipe',id=id))

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/like/<int:id>', methods=['POST','GET'])
@login_required
def likePost(id):
    flag=0
    post_likes = likes.query.filter_by(post_receipe_id=id)
    main_post=post_receipe.query.get(id)


    if post_likes is None:
        add_likes=likes(user_id=current_user.id,post_receipe_id=id,like=1)
        db.session.add(add_likes)
        main_post.likes+=1
        db.session.commit()
    else:
        for li in post_likes:
            if li.user_id==current_user.id:
                flag=1
        if flag==0:
            add_likes=likes(user_id=current_user.id,post_receipe_id=id,like=1)
            db.session.add(add_likes)
            main_post.likes+=1
            db.session.commit()
        
    return redirect(url_for('getReceipe',id=id))
    
@app.route("/showdata")
@login_required
def showData():
    data=post_receipe.query.filter_by(user_id=current_user.id)
    return render_template('showData.html',data=data)


with app.app_context():
    db.create_all()

app.run(debug=True)
