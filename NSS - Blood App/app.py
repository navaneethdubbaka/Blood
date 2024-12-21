from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Function to initialize the database
def init_db():
    conn = sqlite3.connect('donors.db')
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
    conn.close()

init_db()

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route for the registration page
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        # Fetch form data
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phoneno')
        blood_group = request.form.get('bloodgroup')
        location = request.form.get('location')

        # Insert data into the database
        conn = sqlite3.connect('donors.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO donors (name, email, phone, blood_group, location)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, email, phone, blood_group, location))
        conn.commit()
        conn.close()

        # Redirect to the home page after submission
        return redirect(url_for('home'))
    return render_template('registration.html')

# Route for seeking blood donation
@app.route('/seek-donation', methods=['GET'])
def seek_donation():
    blood_group = request.args.get('bloodGroup')
    if blood_group:
        # Query database for matching blood group
        conn = sqlite3.connect('donors.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT name, location, phone FROM donors WHERE blood_group = ?
        ''', (blood_group,))
        donors = cursor.fetchall()
        conn.close()

        # Return the results in a table
        return render_template('donors_list.html', donors=donors, blood_group=blood_group)
    return "No Blood Group specified."

if __name__ == '__main__':
    app.run(debug=True)
