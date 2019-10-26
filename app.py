from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return 'Hello World'

@app.route('/chat')
def chat():
    return render_template('chat.html')

@socketio.on('text', namespace = '/chat')
def message(msg):
    emit('message', {'msg': msg['msg']}, broadcast = True)

if __name__ == '__main__':
    socketio.run(app)