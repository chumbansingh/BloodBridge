from flask import Flask, render_template, request, redirect, session, flash
import mysql.connector
from geopy.distance import geodesic

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sql@2005NOV",
    database="bloodbridge"
)
cursor = conn.cursor(dictionary=True)

# Home Page
@app.route('/')
def home():
    return render_template('home.html')

# Donate Page
@app.route('/donate', methods=['GET', 'POST'])
def donate():
    if request.method == 'POST':
        availability = request.form.get('availability')
        user_id = session.get('user_id')
        cursor.execute("UPDATE users SET availability=%s WHERE id=%s", (availability, user_id))
        conn.commit()
        flash("Donation status updated!", "success")
        return redirect('/')
    return render_template('donate.html')

# Blood Request Page
@app.route('/request', methods=['GET', 'POST'])
def request_blood():
    if request.method == 'POST':
        blood_group = request.form.get('blood_group')
        cursor.execute("SELECT name, blood_group, location FROM users WHERE role='donor' AND availability='yes' AND blood_group=%s", (blood_group,))
        donors = cursor.fetchall()
        return render_template('request.html', donors=donors)
    return render_template('request.html')

# Reward Page
@app.route("/reward")
def reward():
    return render_template("reward.html")

# About Page
@app.route('/about')
def about():
    return render_template('about.html')

# Contact Page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Profile Page
@app.route('/profile')
def profile():
    return render_template('p1.html')

# Nearby donor search
@app.route('/nearby', methods=['POST'])
def nearby():
    try:
        user_lat = float(request.form['latitude'])
        user_lon = float(request.form['longitude'])

        cursor.execute("SELECT name, blood_group, location, latitude, longitude FROM users WHERE role='donor' AND availability='yes'")
        donors = cursor.fetchall()

        nearby_donors = []
        for donor in donors:
            if donor['latitude'] is not None and donor['longitude'] is not None:
                distance = geodesic((user_lat, user_lon), (donor['latitude'], donor['longitude'])).km
                if distance <= 10:
                    nearby_donors.append(donor)

        return render_template('request.html', donors=nearby_donors)

    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
        return redirect('/request')

if __name__ == '__main__':
    app.run(debug=True)