from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import gspread
from oauth2client.service_account import ServiceAccountCredentials


app = Flask(__name__)

# SQLite database connection
conn = sqlite3.connect('TrainingFormSubmissions.db')
cursor = conn.cursor()

# Create the table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS TrainingFormSubmissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        training_type TEXT NOT NULL,
        full_name TEXT NOT NULL,
        email VARCHAR NOT NULL,
        phone_number INTEGER NOT NULL,
        address VARCHAR NOT NULL,
        profession TEXT NOT NULL,
        submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
''')
conn.commit()

# Close the database connection
conn.close()

@app.route('/')
def index():
    title = "Training Form"
    return render_template('training_form.html', title=title)

@app.route('/submit_form', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        training_type = request.form['training_type'] 
        full_name = request.form['full_name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        address = request.form['address']
        profession = request.form['profession']
        

        # Connect to SQLite database
        conn = sqlite3.connect('TrainingFormSubmissions.db')
        cursor = conn.cursor()

        # Check if the email already exists
        cursor.execute('SELECT email FROM TrainingFormSubmissions WHERE email = ?', (email,))
        existing_email = cursor.fetchone()

        if existing_email:
            conn.commit()
            conn.close()
            return redirect(url_for('email_exists'))

        # Insert form data into the database
        cursor.execute('''
            INSERT INTO TrainingFormSubmissions (training_type, full_name, email, phone_number, address, profession)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (training_type, full_name, email, phone_number, address, profession))

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        # Connect to Google Sheets
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('ace-connection-415508-007944cf7dfb.json', scope)
        client = gspread.authorize(creds)

        # Open the Google Sheet by title
        sheet = client.open('TRAINING FORM').sheet1

        # Append the form data to the Google Sheet
        sheet.append_row([training_type, full_name, email, phone_number, address, profession])

        # Redirect to the thank-you page
        return redirect(url_for('typage'))

@app.route('/typage')
def typage():
    return render_template('typage.html')

@app.route('/email_exists')
def email_exists():
    return render_template('email_exists.html')

if __name__ == '__main__':
    app.run(debug=True)

# Note: Need enable sa google console google drive + google sheets API
