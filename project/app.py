from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_socketio import SocketIO, emit
import bcrypt
import json
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'
socketio = SocketIO(app)

USERS_FILE = 'users.json'
connected_users = {}  # username -> sid

# Load users
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, 'w') as f:
        json.dump({}, f)

def load_users():
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

@app.route('/')
def index():
    if 'username' in session:
        return redirect('/chat')
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        users = load_users()

        if username in users:
            return render_template('register.html', error="Username already exists.")
        
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())
        users[username] = hashed.decode('utf-8')
        save_users(users)
        return redirect('/login')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        users = load_users()

        if username in users and bcrypt.checkpw(password, users[username].encode('utf-8')):
            session['username'] = username
            return redirect('/chat')
        return render_template('login.html', error="Invalid credentials.")
    
    return render_template('login.html')

@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect('/login')
    return render_template('chat.html', username=session['username'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# ========== Socket.IO Events ==========

@socketio.on('connect')
def on_connect():
    print("Client connected:", request.sid)

@socketio.on('register_socket')
def handle_register_socket(data):
    username = data.get('username')
    if username:
        connected_users[username] = request.sid
        print(f"User '{username}' registered with SID: {request.sid}")

@socketio.on('send_message')
def handle_private_message(data):
    sender = data.get('from')
    recipient = data.get('to')
    message = data.get('message')

    print(f"Message from {sender} to {recipient}: {message}")
    print(f"Connected users: {connected_users}")

    if recipient in connected_users:
        recipient_sid = connected_users[recipient]
        emit('receive_message', {
            'from': sender,
            'message': message
        }, room=recipient_sid)
    else:
        print(f"Recipient {recipient} not connected.")

# ======================================

if __name__ == '__main__':
    socketio.run(app, debug=True)
