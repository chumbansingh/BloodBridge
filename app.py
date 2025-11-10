from flask import Flask, render_template, request, redirect, session, flash , url_for 

import mysql.connector ,random, string , re 
app = Flask(__name__)
app.secret_key = 'supersecretkey'

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'pass123'
# MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sql@2005NOV",
    database="bloodbridge"
)
cursor = conn.cursor(dictionary=True)
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

# login/signup
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip()
        password = request.form["password"].strip()

        # ✅ Backend validation
        if not re.match(r'^[a-zA-Z0-9._%+-]+@gmail\.com$', email):
            flash("Only valid Gmail addresses are allowed (e.g., yourname@gmail.com).", "danger")
            return redirect(url_for("login"))

        if not re.match(r"^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$", password):
            flash("Password format invalid.", "danger")
            return redirect(url_for("login"))

        # ✅ Check credentials (changed usersignup → users)
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()

        if user:
            session["user_id"] = user["user_id"]
            session["user_name"] = user["name"]
            flash("Login successful!", "success")
            return redirect(url_for("homee"))  # or your home page route
        else:
            flash("Invalid Gmail or Password!", "danger")
            return redirect(url_for("login"))

    return render_template("login.html")
@app.route("/homee")
def homee():
    # Ensure user is logged in
    if "user_id" not in session:
        flash("Please log in to continue.", "warning")
        return redirect(url_for("login"))

    # Pass user data to the template
    return render_template(
        "homee.html",
        user_name=session.get("user_name"),
        user_id=session.get("user_id")
    )

# --- Function to generate user ID ---
def generate_user_id():
    cursor.execute("SELECT COUNT(*) FROM users")
    result = cursor.fetchone()
    
    # handle empty table or dict-style cursor
    if result is None:
        count = 0
    elif isinstance(result, dict):
        count = list(result.values())[0]
    else:
        count = result[0]
        
    return f"BB{count + 1:05d}"

# ✅ SIGNUP ROUTE
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["username"].strip()
        email = request.form["email"].strip()
        password = request.form["password"].strip()
        phone = request.form["phone"].strip()

        # 🔹 Validation checks
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

        # 🔹 Check if email already exists
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            flash("This Gmail is already registered.", "danger")
            return redirect(url_for("signup"))

        # 🔹 Insert user
        user_id = generate_user_id()
        cursor.execute(
            "INSERT INTO users (user_id, name, email, password, phone) VALUES (%s, %s, %s, %s, %s)",
            (user_id, name, email, password, phone)
        )
        conn.commit()

        # ✅ After successful signup, render thank-you page
        return render_template("signupsuccessfull.html", user_id=user_id, name=name)

    return render_template("signup.html")
# Home Page
@app.route('/')
def home():
    return render_template('home.html')


# Donate Page
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

        # ✅ Step 1: Verify if user_id and email exist together in users table
        cursor.execute("SELECT * FROM users WHERE user_id = %s AND email = %s", (user_id, email))
        user = cursor.fetchone()

        if not user:
            #flash("❌ Invalid User ID or Email! Please use your registered credentials.", "danger")
            return render_template("invalid.html")


        # ✅ Step 2: Check for duplicate donation
        cursor.execute("SELECT * FROM donors WHERE user_id = %s", (user_id,))
        if cursor.fetchone():
            #flash("⚠️ You’ve already submitted a donation request! Please wait for admin approval.", "warning")
            return render_template("duplicate.html")


        # ✅ Step 3: Insert donor info
        cursor.execute("""
            INSERT INTO donors (user_id, name, email, address, blood_type, phone, age, times_donated, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (user_id, name, email, address, blood_type, phone, age, 0, "pending"))
        conn.commit()

        # ✅ Step 4: Redirect to a nice thank-you page
        return render_template("thankyou.html", email=email, user_id=user_id)

    return render_template("donate.html")
#request Blood Page
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

        # ✅ Verify user ID and email
        cursor.execute("SELECT * FROM users WHERE user_id = %s AND email = %s", (user_id, email))
        user = cursor.fetchone()

        if not user:
            #flash("❌ Invalid User ID or Email mismatch. Please use your registered account.", "danger")
            return render_template("notuser.html")


        # ✅ Search matching donors
        cursor.execute("""
            SELECT * FROM donors
            WHERE blood_type = %s
            AND address LIKE %s
            AND status = 'approved'
        """, (blood_type, f"%{location}%"))
        donors = cursor.fetchall()

        #flash("✅ Your request has been submitted successfully.", "success")
        return render_template("results.html", donors=donors, blood_type=blood_type, location=location)

    return render_template("request.html")
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

# Donor List Page (Approved wala Donors matra)
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