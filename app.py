from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3

app = Flask(__name__, static_folder='static')
app.config['REGISTRATION_DATABASE'] = 'registration.db'  # Database for registrations
app.config['SESSION_DATABASE'] = 'sessionbook.db'  # Database for session bookings

# Function to get a database connection for registrations
def get_registration_db():
    if 'registration_db' not in g:
        g.registration_db = sqlite3.connect(app.config['REGISTRATION_DATABASE'])
        g.registration_db.row_factory = sqlite3.Row
    return g.registration_db

# Function to get a database connection for session bookings
def get_session_db():
    if 'session_db' not in g:
        g.session_db = sqlite3.connect(app.config['SESSION_DATABASE'])
        g.session_db.row_factory = sqlite3.Row
    return g.session_db

# Function to close the registration database connection
def close_registration_db(e=None):
    db = g.pop('registration_db', None)
    if db is not None:
        db.close()

# Function to close the session database connection
def close_session_db(e=None):
    db = g.pop('session_db', None)
    if db is not None:
        db.close()

# Initialize the registration database
def init_registration_db():
    with app.app_context():
        db = get_registration_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS registrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone_number TEXT NOT NULL,
                message TEXT NOT NULL
            )
        ''')
        db.commit()

# Initialize the session booking database
def init_session_db():
    with app.app_context():
        db = get_session_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                address TEXT NOT NULL,
                age INTEGER NOT NULL,
                weight REAL NOT NULL,
                gender TEXT NOT NULL,
                session_date DATE NOT NULL
            )
        ''')
        db.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        # Retrieve form data for registration
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        message = request.form.get('message')

        try:
            db = get_registration_db()
            cursor = db.cursor()

            # Execute an SQL INSERT statement to insert registration data into the table
            cursor.execute('''
                INSERT INTO registrations (first_name, last_name, email, phone_number, message)
                VALUES (?, ?, ?, ?, ?)
            ''', (first_name, last_name, email, phone_number, message))

            db.commit()  # Commit the transaction
            cursor.close()

            success_message = "Registration successful!"
            return render_template('success.html', message=success_message)
        except sqlite3.Error as e:
            return "An error occurred while registering: " + str(e)
        finally:
            close_registration_db()

    return redirect(url_for('index'))

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        # Process payment data
        card_number = request.form.get('card_number')
        card_holder = request.form.get('card_holder')
        expiration_date = request.form.get('expiration_date')
        cvv = request.form.get('cvv')

        # Insert payment data into the database (carddetail.db)
        insert_payment_data(card_number, card_holder, expiration_date, cvv)

        success_message = "Payment successful!"
        return render_template('payment_confirmation.html',
                               card_number=card_number,
                               card_holder=card_holder,
                               expiration_date=expiration_date,
                               cvv=cvv,
                               message=success_message)
    else:
        return render_template('payment.html')

def insert_payment_data(card_number, card_holder, expiration_date, cvv):
    try:
        conn = sqlite3.connect('carddetail.db')
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS carddetail (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                card_number TEXT NOT NULL,
                card_holder TEXT NOT NULL,
                expiration_date TEXT NOT NULL,
                cvv TEXT NOT NULL
            )
        ''')

        cursor.execute('''
            INSERT INTO carddetail (card_number, card_holder, expiration_date, cvv)
            VALUES (?, ?, ?, ?)
        ''', (card_number, card_holder, expiration_date, cvv))

        conn.commit()
        conn.close()

    except Exception as e:
        print("Error inserting payment data:", str(e))

@app.route('/freesession', methods=['GET', 'POST'])
def freesession():
    if request.method == 'POST':
        # Retrieve form data for session booking
        name = request.form.get('name')
        address = request.form.get('address')
        age = request.form.get('age')
        weight = request.form.get('weight')
        gender = request.form.get('gender')
        session_date = request.form.get('session_date')
        
        # Insert session booking data into the database (sessionbook.db)
        insert_session_data(name, address, age, weight, gender, session_date)
        
        success_message = f"Session booked for {session_date}"
        return render_template('confirmedsession.html', message=success_message)
    
    return render_template('freesession.html')

@app.route('/book_session', methods=['POST'])
def book_session():
    if request.method == 'POST':
        # Retrieve form data for session booking
        name = request.form.get('name')
        address = request.form.get('address')
        age = request.form.get('age')
        weight = request.form.get('weight')
        gender = request.form.get('gender')
        session_date = request.form.get('session_date')
        
        # Insert session booking data into the database (sessionbook.db)
        insert_session_data(name, address, age, weight, gender, session_date)
        
        success_message = f"Session booked for {session_date}"
        return render_template('confirmedsession.html', message=success_message)
    
    return redirect(url_for('freesession'))

# ... (previous code)

# Function to insert session booking data into the sessionbook database
def insert_session_data(name, address, age, weight, gender, session_date):
    try:
        db = get_session_db()
        cursor = db.cursor()

        cursor.execute('''
            INSERT INTO sessions (name, address, age, weight, gender, session_date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, address, age, weight, gender, session_date))

        db.commit()
        cursor.close()
    except sqlite3.Error as e:
        print("Error inserting session data:", str(e))
    finally:
        close_session_db()

# ... (rest of the code)


if __name__ == '__main__':
    init_registration_db()  # Initialize the registration database
    init_session_db()      # Initialize the session booking database
    app.run(debug=True)
