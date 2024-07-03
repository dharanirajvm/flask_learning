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

def get_courses(branch):
    # Sample courses with images and descriptions
    sample_courses = {
        "Computer Science": [
            {"name": "Introduction to Programming", "image": "path/to/image1.jpg", "description": "Learn the basics of programming using Python."},
            {"name": "Data Structures", "image": "path/to/image2.jpg", "description": "Understand the fundamental data structures in computer science."},
            {"name": "Algorithms", "image": "path/to/image3.jpg", "description": "Explore algorithm design and analysis techniques."},
            {"name": "Operating Systems", "image": "path/to/image4.jpg", "description": "Study the principles of modern operating systems."},
            {"name": "Databases", "image": "path/to/image5.jpg", "description": "Learn about database management systems and SQL."},
            {"name": "Computer Networks", "image": "path/to/image6.jpg", "description": "Understand the fundamentals of computer networking."},
            {"name": "Software Engineering", "image": "path/to/image7.jpg", "description": "Explore software development methodologies and practices."},
            {"name": "Artificial Intelligence", "image": "path/to/image8.jpg", "description": "Study the basics of artificial intelligence and machine learning."},
            {"name": "Machine Learning", "image": "path/to/image9.jpg", "description": "Learn about machine learning algorithms and applications."},
            {"name": "Computer Graphics", "image": "path/to/image10.jpg", "description": "Understand the principles of computer graphics and visualization."}
        ],
        "Electrical Engineering": [
            {"name": "Circuits", "image": "path/to/image1.jpg", "description": "Learn the basics of electrical circuits and components."},
            {"name": "Electromagnetics", "image": "path/to/image2.jpg", "description": "Study electromagnetic fields and their applications."},
            {"name": "Signal Processing", "image": "path/to/image3.jpg", "description": "Understand the principles of signal processing techniques."},
            {"name": "Control Systems", "image": "path/to/image4.jpg", "description": "Explore the design and analysis of control systems."},
            {"name": "Microelectronics", "image": "path/to/image5.jpg", "description": "Learn about microelectronic devices and circuits."},
            {"name": "Power Systems", "image": "path/to/image6.jpg", "description": "Understand the fundamentals of power generation and distribution."},
            {"name": "Communication Systems", "image": "path/to/image7.jpg", "description": "Study the principles of communication systems."},
            {"name": "Digital Systems", "image": "path/to/image8.jpg", "description": "Learn about digital logic design and systems."},
            {"name": "Analog Electronics", "image": "path/to/image9.jpg", "description": "Understand the design and analysis of analog circuits."},
            {"name": "Embedded Systems", "image": "path/to/image10.jpg", "description": "Explore the fundamentals of embedded systems design."}
        ],
        "Mechanical Engineering": [
            {"name": "Thermodynamics", "image": "path/to/image1.jpg", "description": "Learn the principles of thermodynamics and their applications."},
            {"name": "Fluid Mechanics", "image": "path/to/image2.jpg", "description": "Understand the behavior of fluids in various conditions."},
            {"name": "Solid Mechanics", "image": "path/to/image3.jpg", "description": "Study the mechanics of solid materials and structures."},
            {"name": "Dynamics", "image": "path/to/image4.jpg", "description": "Explore the principles of dynamics and motion analysis."},
            {"name": "Heat Transfer", "image": "path/to/image5.jpg", "description": "Learn about the mechanisms of heat transfer."},
            {"name": "Manufacturing Processes", "image": "path/to/image6.jpg", "description": "Understand the various manufacturing processes and techniques."},
            {"name": "Mechanical Design", "image": "path/to/image7.jpg", "description": "Study the principles of mechanical design and analysis."},
            {"name": "Robotics", "image": "path/to/image8.jpg", "description": "Explore the fundamentals of robotics and automation."},
            {"name": "Materials Science", "image": "path/to/image9.jpg", "description": "Learn about the properties and behavior of materials."},
            {"name": "Vibration Analysis", "image": "path/to/image10.jpg", "description": "Understand the analysis and control of vibrations."}
        ],
        # Add more branches and their courses as needed
    }
    return sample_courses.get(branch, [])

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
