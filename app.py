from flask import Flask, render_template, request, redirect, session, flash , url_for 

import mysql.connector ,re 
app = Flask(__name__)
app.secret_key = 'supersecretkey'

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'pass123'

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sql@2005NOV",
    database="bloodbridge"
)
cursor = conn.cursor(dictionary=True)

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


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip()
        password = request.form["password"].strip()


        if not re.match(r'^[a-zA-Z0-9._%+-]+@gmail\.com$', email):
            flash("Only valid Gmail addresses are allowed (e.g., yourname@gmail.com).", "danger")
            return redirect(url_for("login"))

        if not re.match(r"^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$", password):
            flash("Password format invalid.", "danger")
            return redirect(url_for("login"))


        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()

        if user:
            session["user_id"] = user["user_id"]
            session["user_name"] = user["name"]
            #flash("Login successful!", "success")
            return redirect(url_for("homee"))  
        else:
            flash("Invalid Gmail or Password!", "danger")
            return redirect(url_for("login"))

    return render_template("login.html")
@app.route("/homee")
def homee():

    if "user_id" not in session:
        flash("Please log in to continue.", "warning")
        return redirect(url_for("login"))


    return render_template(
        "homee.html",
        user_name=session.get("user_name"),
        user_id=session.get("user_id")
    )


def generate_user_id():
    cursor.execute("SELECT COUNT(*) FROM users")
    result = cursor.fetchone()
    

    if result is None:
        count = 0
    elif isinstance(result, dict):
        count = list(result.values())[0]
    else:
        count = result[0]
        
    return f"BB{count + 1:05d}"


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["username"].strip()
        email = request.form["email"].strip()
        password = request.form["password"].strip()
        phone = request.form["phone"].strip()


        if not re.match(r"^[A-Za-z\s]+$", name):
            flash("Invalid name: only letters and spaces allowed.", "danger")
            return redirect(url_for("signup"))

        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            flash("Invalid email format.", "danger")
            return redirect(url_for("signup"))

        if not re.match(r"^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$", password):
            flash("Password must be 8+ chars, 1 uppercase, 1 number, and 1 special character.", "danger")
            return redirect(url_for("signup"))

        if not re.match(r"^[0-9]{10}$", phone):
            flash("Phone number must be 10 digits.", "danger")
            return redirect(url_for("signup"))


        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            flash("This Gmail is already registered.", "danger")
            return redirect(url_for("signup"))


        user_id = generate_user_id()
        cursor.execute(
            "INSERT INTO users (user_id, name, email, password, phone) VALUES (%s, %s, %s, %s, %s)",
            (user_id, name, email, password, phone)
        )
        conn.commit()


        return render_template("signupsuccessfull.html", user_id=user_id, name=name)

    return render_template("signup.html")

@app.route('/')
def home():
    return render_template('home.html')



@app.route("/donate", methods=["GET", "POST"])
def donate():
    if request.method == "POST":
        user_id = request.form["user_id"].strip()
        email = request.form["email"].strip()
        name = request.form["name"].strip()
        address = request.form["address"].strip()
        blood_type = request.form["blood_type"].strip()
        phone = request.form["phone"].strip()
        age = request.form["age"].strip()


        cursor.execute("SELECT * FROM users WHERE user_id = %s AND email = %s", (user_id, email))
        user = cursor.fetchone()

        if not user:
            #flash(" Invalid User ID or Email! Please use your registered credentials.", "danger")
            return render_template("invalid.html")



        cursor.execute("SELECT * FROM donors WHERE user_id = %s", (user_id,))
        if cursor.fetchone():
            #flash(" You’ve already submitted a donation request! Please wait for admin approval.", "warning")
            return render_template("duplicate.html")



        cursor.execute("""
            INSERT INTO donors (user_id, name, email, address, blood_type, phone, age, times_donated, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (user_id, name, email, address, blood_type, phone, age, 0, "pending"))
        conn.commit()


        return render_template("thankyou.html", email=email, user_id=user_id)

    return render_template("donate.html")

@app.route('/request', methods=['GET', 'POST'])
def request_blood():
    if request.method == 'POST':
        user_id = request.form['user_id']
        email = request.form['email']
        blood_type = request.form['blood_type']
        location = request.form['location']
        patient_name = request.form['patient_name']
        urgency = request.form['urgency']
        contact = request.form['contact']


        cursor.execute("SELECT * FROM users WHERE user_id = %s AND email = %s", (user_id, email))
        user = cursor.fetchone()

        if not user:
            #flash("❌ Invalid User ID or Email mismatch. Please use your registered account.", "danger")
            return render_template("notuser.html")



        cursor.execute("""
            SELECT * FROM donors
            WHERE blood_type = %s
            AND address LIKE %s
            AND status = 'approved'
        """, (blood_type, f"%{location}%"))
        donors = cursor.fetchall()


        return render_template("results.html", donors=donors, blood_type=blood_type, location=location)

    return render_template("request.html")

@app.route('/about')
def about():
    return render_template('about.html')


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


@app.route('/donors')
def donor_list():
    cursor.execute("SELECT * FROM donors WHERE status='approved'")
    donors = cursor.fetchall()
    return render_template("donors.html", donors=donors)


@app.route("/admin")
def admin_panel():
    if not session.get('admin_logged_in'):
        return redirect('/admin-login')

    cursor.execute("SELECT * FROM donors WHERE status = 'pending'")
    pending_donors = cursor.fetchall()

    cursor.execute("SELECT * FROM messages ORDER BY timestamp DESC")
    contact_messages = cursor.fetchall()

    return render_template("admin.html", pending_donors=pending_donors, messages=contact_messages)

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect('/admin-login')


@app.route("/approve/<int:id>", methods=["POST"])
def approve_donor(id):
    cursor.execute("UPDATE donors SET status='approved' WHERE id=%s", (id,))
    conn.commit()
    return redirect("/admin")


@app.route("/reject/<int:id>", methods=["POST"])
def reject_donor(id):
    cursor.execute("UPDATE donors SET status='rejected' WHERE id=%s", (id,))
    conn.commit()
    return redirect("/admin")


@app.route('/send_request', methods=['POST'])
def send_request():
    if 'user_id' not in session:
        return redirect('/login')

    sender_id = session['user_id']
    receiver_id = request.form['receiver_id']

    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO notifications (sender_id, receiver_id, status)
        VALUES (%s, %s, 'pending')
    """, (sender_id, receiver_id))
    conn.commit()

    return redirect('/donors?msg=request_sent')

@app.route('/notifications')
def notifications():
    if 'user_id' not in session:
        flash('Please log in first to view notifications.')
        return redirect('/login')

    user_id = session['user_id']
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT n.id, u.name AS sender_name, u.email AS sender_email, n.status, n.created_at
        FROM notifications n
        JOIN users u ON n.sender_id = u.user_id
        WHERE n.receiver_id = %s
        ORDER BY n.created_at DESC
    """, (user_id,))
    notifications = cursor.fetchall()

    return render_template('notifications.html', notifications=notifications)

@app.route('/update_request/<int:request_id>/<action>')
def update_request(request_id, action):
    if action not in ['accepted', 'rejected']:
        flash('Invalid action.')
        return redirect('/notifications')

    cursor = conn.cursor()
    cursor.execute("UPDATE notifications SET status=%s WHERE id=%s", (action, request_id))
    conn.commit()

    flash(f'Request {action} successfully!')
    return redirect('/notifications')
@app.route('/my_requests')
def my_requests():
    if 'user_id' not in session:
        flash('Please log in first to view your requests.')
        return redirect('/login')

    user_id = session['user_id']
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT n.id, u.name AS receiver_name, u.email AS receiver_email, n.status, n.created_at
        FROM notifications n
        JOIN users u ON n.receiver_id = u.user_id
        WHERE n.sender_id = %s
        ORDER BY n.created_at DESC
    """, (user_id,))
    requests = cursor.fetchall()

    return render_template('my_requests.html', requests=requests)
@app.route('/delete_request/<int:request_id>', methods=['POST'])
def delete_request(request_id):
    if 'user_id' not in session:
        flash('Please log in first.')
        return redirect('/login')

    cursor = conn.cursor()
    cursor.execute("DELETE FROM notifications WHERE id = %s", (request_id,))
    conn.commit()
    flash('Request deleted successfully!')
    return redirect(request.referrer)  

if __name__ == '__main__':
    app.run(debug=True)