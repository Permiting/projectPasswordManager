from flask import Flask, request, render_template, redirect, url_for, session
import sqlite3
import hashlib
import os
from cryptography.fernet import Fernet

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Generate or load encryption key
def load_key():
    if not os.path.exists("key.key"):
        key = Fernet.generate_key()
        with open("key.key", "wb") as key_file:
            key_file.write(key)
    else:
        with open("key.key", "rb") as key_file:
            key = key_file.read()
    return key

encryption_key = load_key()
cipher = Fernet(encryption_key)

# Database setup
def initialize_db():
    conn = sqlite3.connect("password_manager.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY, 
                        username TEXT UNIQUE, 
                        password TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS passwords (
                        id INTEGER PRIMARY KEY,
                        user_id INTEGER,
                        service TEXT,
                        password TEXT,
                        FOREIGN KEY(user_id) REFERENCES users(id))''')
    conn.commit()
    conn.close()

initialize_db()

# Secure password hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(hashed_password, password):
    return hashed_password == hashlib.sha256(password.encode()).hexdigest()

# Encrypt and decrypt passwords
def encrypt_password(password):
    return cipher.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password):
    return cipher.decrypt(encrypted_password.encode()).decode()

# Routes
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    conn = sqlite3.connect("password_manager.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                       (username, hash_password(password)))
        conn.commit()
    except sqlite3.IntegrityError:
        return "Username already exists."
    finally:
        conn.close()
    return redirect(url_for('home'))

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    conn = sqlite3.connect("password_manager.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, password FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    if user and check_password(user[1], password):
        session['user_id'] = user[0]
        return redirect(url_for('dashboard'))
    return "Invalid credentials."

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('home'))
    
    conn = sqlite3.connect("password_manager.db")
    cursor = conn.cursor()
    cursor.execute("SELECT service, password FROM passwords WHERE user_id = ?", (session['user_id'],))
    passwords = [(service, decrypt_password(password)) for service, password in cursor.fetchall()]
    conn.close()

    return render_template("dashboard.html", passwords=passwords)

@app.route('/store', methods=['POST'])
def store_password():
    if 'user_id' not in session:
        return redirect(url_for('home'))
    service = request.form['service']
    password = request.form['password']
    encrypted_password = encrypt_password(password)
    conn = sqlite3.connect("password_manager.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO passwords (user_id, service, password) VALUES (?, ?, ?)",
                   (session['user_id'], service, encrypted_password))
    conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))

@app.route('/retrieve')
def retrieve_passwords():
    if 'user_id' not in session:
        return redirect(url_for('home'))
    conn = sqlite3.connect("password_manager.db")
    cursor = conn.cursor()
    cursor.execute("SELECT service, password FROM passwords WHERE user_id = ?", (session['user_id'],))
    passwords = [(service, decrypt_password(password)) for service, password in cursor.fetchall()]
    conn.close()
    return render_template("dashboard.html", passwords=passwords)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
