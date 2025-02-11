from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(_name_)

DATABASE = "donors.db"

# Function to get a database connection
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Enables dictionary-like access to results
    return conn

# Function to initialize the database
def init_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS donors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                blood_group TEXT NOT NULL,
                location TEXT NOT NULL
            )
        ''')
        conn.commit()

# Initialize the database at startup
init_db()

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route for donor registration
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phoneno')
        blood_group = request.form.get('bloodgroup')
        location = request.form.get('location')

        if not all([name, email, phone, blood_group, location]):
            return "All fields are required!", 400  # Bad request error

        # Insert data into the database
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO donors (name, email, phone, blood_group, location)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, email, phone, blood_group, location))
            conn.commit()

        return redirect(url_for('home'))

    return render_template('registration.html')

# Route for seeking blood donation
@app.route('/seek-donation', methods=['GET'])
def seek_donation():
    blood_group = request.args.get('bloodGroup')

    if not blood_group:
        return "No Blood Group specified.", 400

    # Query database for matching donors
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT name, location, phone FROM donors WHERE blood_group = ?
        ''', (blood_group,))
        donors = cursor.fetchall()

    return render_template('donors_list.html', donors=donors, blood_group=blood_group)

if _name_ == '_main_':
    port = int(os.environ.get('PORT', 5000))  # Uses Vercel's assigned port or defaults to 5000
    app.run(host='0.0.0.0', port=port, debug=True)
