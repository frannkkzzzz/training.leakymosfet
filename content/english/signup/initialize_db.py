import sqlite3

conn = sqlite3.connect('TrainingFormSubmissions.db')
cursor = conn.cursor()

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
conn.close()
