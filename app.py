from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from db_config import connect_db
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# A secret key is required for sessions to work
app.config['SECRET_KEY'] = 'your_super_secret_key_change_this'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# --- Main Routes ---
@app.route("/")
def index():
    return render_template("index.html")

# --- Authentication Routes ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Hash the password for security
        hashed_password = generate_password_hash(password)

        db = connect_db()
        cursor = db.cursor(dictionary=True)

        # Check if user already exists
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user:
            flash("هذا البريد الإلكتروني مسجل بالفعل.")
            return redirect(url_for('register'))

        # Insert new user into the database
        cursor.execute("INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)",
                       (name, email, hashed_password))
        db.commit()
        cursor.close()
        db.close()

        flash("تم التسجيل بنجاح! يمكنك الآن تسجيل الدخول.")
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        db = connect_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        db.close()

        if user and check_password_hash(user['password_hash'], password):
            # Login successful, store user info in session
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            return redirect(url_for('espace_telmoudi'))
        else:
            flash('البريد الإلكتروني أو كلمة المرور غير صحيحة.')

    return render_template('login.html')

@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    return redirect(url_for('index'))


# --- Protected User Routes ---
@app.route("/espace")
def espace_telmoudi():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    # Pass the user's name to the template
    user_name = session.get('user_name', 'زائر') # 'زائر' is a fallback
    return render_template("espace.html", user_name=user_name)


@app.route("/account-settings", methods=['GET', 'POST'])
def account_settings():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    db = connect_db()
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        # This is for updating the user's data
        name = request.form['name']
        email = request.form['email']
        
        cursor.execute("UPDATE users SET name = %s, email = %s WHERE id = %s", (name, email, user_id))
        db.commit()
        
        # Update the name in the session as well
        session['user_name'] = name
        
        flash("تم تحديث معلومات الحساب بنجاح!", "success")
        return redirect(url_for('account_settings'))

    # This is for displaying the user's current data
    cursor.execute("SELECT name, email FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    db.close()
    
    return render_template("account_settings.html", user=user)


def save_to_db(name, email, opinion, media_path, media_type, user_id):
    db = connect_db()
    cursor = db.cursor()
    # Add user_id to the INSERT statement
    cursor.execute("INSERT INTO feedback (name, email, opinion, media_path, media_type, user_id) VALUES (%s, %s, %s, %s, %s, %s)",
                   (name, email, opinion, media_path, media_type, user_id))
    db.commit()
    cursor.close()
    db.close()

@app.route("/submit-feedback", methods=["POST"])
def submit_feedback():
    # If a user is logged in, use their name and ID. Otherwise, use the form's name.
    if 'user_id' in session:
        user_id = session['user_id']
        name = session['user_name']
    else:
        user_id = None
        name = request.form["visitorName"]

    email = request.form["visitorEmail"]
    opinion = request.form["visitorOpinion"]
    file = request.files["visitorMedia"]
    
    media_path = ""
    media_type = ""

    if file and file.filename != "":
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        filename = secure_filename(file.filename)
        media_path = os.path.join('uploads', filename).replace('\\', '/')
        full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(full_path)
        media_type = "video" if "video" in file.content_type else "image"

    # Pass the user_id to the save function
    save_to_db(name, email, opinion, media_path, media_type, user_id)
    
    flash("شكراً على رأيك، تم إرساله بنجاح!", "success")
    return redirect(url_for('feedback'))

# Feedback page
@app.route("/feedback")
def feedback():
    try:
        db = connect_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM feedback ORDER BY submitted_at DESC")
        feedbacks = cursor.fetchall()
        cursor.close()
        db.close()
        return render_template("feedback.html", feedbacks=feedbacks)
    except Exception as e:
        flash("حدث خطأ أثناء تحميل التعليقات.")
        return render_template("feedback.html", feedbacks=[])

# Book appointment page
@app.route("/book-appointment", methods=['GET', 'POST'])
def book_appointment():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        service = request.form['service']
        date = request.form['date']
        user_id = session['user_id']

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO appointments (user_id, service_name, appointment_date) VALUES (%s, %s, %s)",
                       (user_id, service, date))
        db.commit()
        cursor.close()
        db.close()

        flash("تم حجز موعدك بنجاح!", "success")
        return redirect(url_for('my_appointments')) # Redirect to a new page to see all appointments

    return render_template("book_appointment.html")

@app.route("/my-appointments")
def my_appointments():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT id, service_name, appointment_date, status 
        FROM appointments 
        WHERE user_id = %s 
        ORDER BY appointment_date DESC
    """, (user_id,))
    appointments = cursor.fetchall()
    cursor.close()
    db.close()

    return render_template("my_appointments.html", appointments=appointments)

@app.route("/my-feedback")
def my_feedback():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT opinion, media_path, media_type, submitted_at FROM feedback WHERE user_id = %s ORDER BY submitted_at DESC", (user_id,))
    feedbacks = cursor.fetchall()
    cursor.close()
    db.close()
    
    return render_template("my_feedback.html", feedbacks=feedbacks)

@app.route('/cancel-appointment/<int:appointment_id>', methods=['POST'])
def cancel_appointment(appointment_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    
    db = connect_db()
    cursor = db.cursor()
    # Security check: Ensure the appointment belongs to the logged-in user before deleting
    cursor.execute("DELETE FROM appointments WHERE id = %s AND user_id = %s", (appointment_id, user_id))
    db.commit()
    cursor.close()
    db.close()
    
    flash("تم إلغاء الموعد بنجاح.", "success")
    return redirect(url_for('my_appointments'))

if __name__ == '__main__':
    # Create uploads directory if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)