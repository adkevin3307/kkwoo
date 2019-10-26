import os
from datetime import timedelta
from flask import Flask, request, render_template, redirect, session
from flask_session import Session
from flask_socketio import SocketIO, emit, send, join_room, leave_room
from flask_migrate import Migrate, MigrateCommand
from redis import Redis

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = Redis(
        host = 'localhost',
        port = 6379)
app.config['SESSION_USE_SINGER'] = True
app.config['SESSION_PERMANENT'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=31)

app.config.from_object(__name__)
Session(app)
socketio = SocketIO(app)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.values['username']
        session['room'] = request.values['room']
    return redirect('/chat')

@app.route('/chat')
def chat():
    username = session.get('username')
    room = session.get('room')
    return render_template('chat.html')

@socketio.on('text', namespace = '/chat')
def message(data):
    username = session.get('username')
    room = session.get('room')
    emit('message', {'msg': username + ': ' + data['msg']}, room = room)

@socketio.on('join', namespace = '/chat')
def on_join(data):
    username = session.get('username')
    room = session.get('room')
    join_room(room)
    emit('message', {'msg': username + ' has entered the room :D'}, room = room)

@socketio.on('leave', namespace = '/chat')
def on_leave(data):
    username = session.get('username')
    room = session.get('room')
    leave_room(room)
    emit('message', {'msg': username + ' has left the room.'}, room = room)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
