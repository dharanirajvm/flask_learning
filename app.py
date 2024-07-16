from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

# MongoDB Atlas Configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/mydatabase"
mongo = PyMongo(app)
users_collection = mongo.db.users

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup_post():
    username = request.form['username']
    reg_no = request.form['reg_no']
    dob = request.form['dob']
    password = request.form['password']

    hashed_password = generate_password_hash(password)
    user_data = {
        'username': username,
        'reg_no': reg_no,
        'dob': dob,
        'password': hashed_password
    }

    users_collection.insert_one(user_data)
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']

    user = users_collection.find_one({'username': username})

    if user and check_password_hash(user['password'], password):
        session['username'] = username  # Store username in session
        return redirect(url_for('dashboard'))
    else:
        return jsonify({'message': 'Invalid username or password'})

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    courses = []
    branch = ''
    if request.method == 'POST':
        branch = request.form['branch']
        courses = get_courses(branch)

    return render_template('dashboard.html', courses=courses, branch=branch)
@app.route('/dashboard1',methods=['GET','POST'])
def dashboard1():
    if request.method=='POST':
        return render_template('enrollment.html')
def get_courses(branch):
    # Connect to MongoDB
    
    courses_collection = mongo.db.courses
    
    # Query the courses collection for the given branch
    courses = list(courses_collection.find({"branch": branch}))
    
    return courses

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
