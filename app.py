from flask import Flask, render_template, request, redirect, session, url_for, flash
import mysql.connector
from geopy.distance import geodesic

app = Flask(__name__)
app.secret_key = 'supersecretkey'

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sql@2005NOV",
    database="bloodbridge"
)
cursor = conn.cursor(dictionary=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        blood_group = request.form['blood_group']
        role = request.form['role']
        location = request.form['location']
        
        cursor.execute(
            "INSERT INTO users (name, email, password, blood_group, role, location, availability) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (name, email, password, blood_group, role, location, 'yes')
        )
        conn.commit()
        
        flash("Registered successfully!", "success")  # <-- Flash message
        return redirect('/login')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()
        if user:
            session['user_id'] = user['id']
            session['role'] = user['role']
            session['name'] = user['name']
            return redirect('/dashboard')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    role = session.get('role')
    if role == 'seeker':
        cursor.execute("SELECT name, blood_group, location FROM users WHERE role='donor' AND availability='yes'")
        donors = cursor.fetchall()
        return render_template('dashboard.html', role=role, donors=donors)
    return render_template('dashboard.html', role=role)

@app.route('/donate', methods=['POST'])
def donate():
    availability = request.form['availability']
    user_id = session.get('user_id')
    cursor.execute("UPDATE users SET availability=%s WHERE id=%s", (availability, user_id))
    conn.commit()
    return redirect('/dashboard')

@app.route('/search')
def search():
    blood_group = request.args.get('blood_group')
    cursor.execute("SELECT name, blood_group, location FROM users WHERE role='donor' AND availability='yes' AND blood_group=%s", (blood_group,))
    donors = cursor.fetchall()
    return render_template('dashboard.html', role='seeker', donors=donors)

@app.route('/nearby', methods=['POST'])
def nearby():
    user_lat = float(request.form['latitude'])
    user_lon = float(request.form['longitude'])
    cursor.execute("SELECT name, blood_group, location, latitude, longitude FROM users WHERE role='donor' AND availability='yes'")
    all_donors = cursor.fetchall()
    nearby_donors = []
    for donor in all_donors:
        if donor['latitude'] is not None and donor['longitude'] is not None:
            dist = geodesic((user_lat, user_lon), (donor['latitude'], donor['longitude'])).km
            if dist <= 10:
                nearby_donors.append(donor)
    return render_template('dashboard.html', role='seeker', donors=nearby_donors)

if __name__ == '__main__':
    app.run(debug=True)