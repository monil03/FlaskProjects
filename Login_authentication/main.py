from flask import Flask, render_template, redirect, request, flash, session, url_for
from pymongo import MongoClient
from flask_bcrypt import Bcrypt

# Initialize Flask app and bcrypt for password hashing
app = Flask(__name__)
bcrypt = Bcrypt(app)

# Set up secret key for sessions
app.secret_key = 'your_API_key'  # Use a unique, secret key

# MongoDB connection
client = MongoClient("mongodb://localhost:27017")  # Replace with your MongoDB URI
db = client.user_authentication  # Replace with your database name
collection = db.users  # Replace with your collection name

# Home route to render the login page
@app.route("/")
def index():
    return render_template('login.html')

# Home route after login
@app.route("/home")
def home():
    if 'username' in session:  # Check if user is logged in
        return render_template('home.html', username=session['username'])
    else:
        # If not logged in, redirect to login page
        return render_template('loginfirst.html')

# Login route that handles login logic
@app.route("/login", methods=['POST','GET'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    emailid = request.form.get('name')
    password = request.form.get('password')
 
    user = collection.find_one({'emailid': emailid})

    # If a user is found, check the password
    if user and bcrypt.check_password_hash(user['password'], password):
        session['emailid'] = user['emailid']
        session['username'] = user['username']
        return redirect(url_for('home'))
    
    return render_template('login.html', message="Invalid credentials, please try again.")
    
   

   
    
@app.route('/signup')
def signup():
    return render_template('register.html')

# Logout route to end the user session
@app.route('/logout')
def logout():
    if 'username' and 'emailid' in session:
        session.pop('emailid', None)  # Remove email from session
        session.pop('username', None)  # Remove username from session
        return render_template('login.html')  # Redirect to login page
    else:
        return '<p>User already logged out</p>'

# Registration route to handle user sign up
@app.route("/register", methods=['POST'])
def register():
    user_data = {
        'emailid': request.form.get('name'),
        'username': request.form.get('username'),
        'password': request.form.get('password')
    }

    # Hash the password before saving to the database
    user_data['password'] = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')

    # Insert the new user into the MongoDB collection
    collection.insert_one(user_data)

    # Redirect to login page after successful registration
    return render_template('login.html')

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
