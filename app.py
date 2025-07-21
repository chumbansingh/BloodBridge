from flask import Flask, render_template, request, redirect, session, flash
import mysql.connector
app = Flask(__name__)
app.secret_key = 'supersecretkey'

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'pass123'
# 4.Admin Login Route
@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect('/admin')
        else:
            flash('Invalid credentials!', 'danger')
    
    return render_template('admin_login.html')

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
@app.route("/donate", methods=["GET", "POST"])
def donate():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        address = request.form["address"]
        blood_type = request.form["blood_type"]
        phone = request.form["phone"]
        age = request.form["age"]

        cursor.execute("""
            INSERT INTO donors (name, email, address, blood_type, phone, age, times_donated, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (name, email, address, blood_type, phone, age, 0, 'pending'))
        conn.commit()
        return render_template("thankyou.html")

    return render_template("donate.html")

@app.route('/request', methods=['GET', 'POST'])
def request_blood():
    if request.method == 'POST':
        blood_type = request.form['blood_type']
        location = request.form['location']

        cursor.execute(
            "SELECT * FROM donors WHERE blood_type = %s AND address LIKE %s AND status = 'approved'",
            (blood_type, f"%{location}%")
        )
        donors = cursor.fetchall()

        # You can also access patient_name, urgency, contact if needed:
        patient_name = request.form['patient_name']
        urgency = request.form['urgency']
        contact = request.form['contact']

        return render_template("results.html", donors=donors, blood_type=blood_type, location=location)

    return render_template("request.html")
# Reward Page
@app.route("/reward")
def reward():
    return render_template("reward.html")

# About Page
@app.route('/about')
def about():
    return render_template('about.html')

# Contact Page
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        cursor.execute("INSERT INTO messages (name, email, message) VALUES (%s, %s, %s)", 
                       (name, email, message))
        conn.commit()
        
    return render_template('contact.html')

# Donor List Page (Approved Donors Only)
@app.route('/donors')
def donor_list():
    cursor.execute("SELECT * FROM donors WHERE status='approved'")
    donors = cursor.fetchall()
    return render_template("donors.html", donors=donors)

# Admin Panel Route
@app.route("/admin")
def admin_panel():
    if not session.get('admin_logged_in'):
        return redirect('/admin-login')

    cursor.execute("SELECT * FROM donors WHERE status = 'pending'")
    pending_donors = cursor.fetchall()

    cursor.execute("SELECT * FROM messages ORDER BY timestamp DESC")
    contact_messages = cursor.fetchall()

    return render_template("admin.html", pending_donors=pending_donors, messages=contact_messages)
#for Admin Logout
@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect('/admin-login')

# Approve Donor
@app.route("/approve/<int:id>", methods=["POST"])
def approve_donor(id):
    cursor.execute("UPDATE donors SET status='approved' WHERE id=%s", (id,))
    conn.commit()
    return redirect("/admin")

# Reject Donor
@app.route("/reject/<int:id>", methods=["POST"])
def reject_donor(id):
    cursor.execute("UPDATE donors SET status='rejected' WHERE id=%s", (id,))
    conn.commit()
    return redirect("/admin")


if __name__ == '__main__':
    app.run(debug=True)