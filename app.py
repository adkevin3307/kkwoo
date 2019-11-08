import os
from datetime import timedelta
from flask import Flask, request, render_template, redirect, session, jsonify
from flask_socketio import SocketIO, emit, send, join_room, leave_room
import kkbox_api
from algorithm import is_suit
from time import time
# from flask_migrate import Migrate, MigrateCommand
# from redis import Redis
# from flask_session import Session

# passwd = open('redis_config.txt', 'r').read()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SESSION_USE_SINGER'] = True
app.config['SESSION_PERMANENT'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days = 31)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.debug = True
# app.config['SESSION_REDIS'] = Redis(
#     host = 'localhost',
#     port = 6379,
#     password = passwd
# )
# app.config['SESSION_TYPE'] = 'redis'
# app.config.from_object(__name__)

# Session(app)
socketio = SocketIO(app)

matching_pool = {}

# @app.errorhandler(404)
# def page_not_found(e):
#     return redirect('/')

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods = ['GET'])
def login():
    return redirect('/chat')

@app.route('/redirect', methods = ['GET'])
def redirect_uri():
    if request.method == 'GET':
        if 'code' in request.args:
            kkbox_api.access_token(request.args['code'])
            kkbox_api.me()
        else:
            return redirect('/index')
    return redirect('/chat')

@app.route('/online')
def online():
    return jsonify({'result': ('user_id' in session)})

@app.route('/match')
def match():
    start = time()
    me = session.get('user_id')
    room = session.get('room')
    for user in matching_pool:
        if is_suit(user, me):
            print('user: {}, me: {}, room: {}'.format(user, me, room))
            socketio.emit(user, {'target_room': room}, broadcast = True, namespace = '/chat')
            # matching_pool.remove(user) # set version pool
            del matching_pool[user]  # dict version pool
            return jsonify({'url': '/chatroom'})
        if time() - matching_pool[user] >= 300:
            del matching_pool[user]
            socketio.emit(user, {'target_room': 'None'}, broadcast = True, namespace = '/chat')
        if time() - start >= 30: # TTL: 30s
            return jsonify({'url': '/sorry'})
    else: # not match in the pool
        matching_pool[me] = time() # dict version pool
        return jsonify({'url': 'waiting'}) # TODO should be result: 'waiting'

@app.route('/sorry')
def sorry():
    return render_template('sorry.html')

@app.route('/chat')
def chat():
    if 'user_id' not in session:
        return redirect('/index')
    return render_template('chat.html')
    
@app.route('/chatroom')
def chatroom():
    if 'user_id' not in session:
        return redirect('/index')
    username = session.get('username')
    print('{} in chatroom'.format(username))
    room = session.get('room')
    return render_template('chatroom.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/get_user')
def get_user():
    return jsonify({'user_id': session.get('user_id')})

@app.route('/post_room', methods = ['POST'])
def post_room():
    if request.method == 'POST':
        session['room'] = request.values['target_room']
        return jsonify({'url': '/chatroom'})

@socketio.on('join', namespace = '/chatroom')
def on_join(data):
    print('{} join'.format(session))
    # username = session.get('username')
    user_id = session.get('user_id')
    room = session.get('room')
    join_room(room)
    emit('message', {'user_id': user_id, 'msg': 'has entered the room :D'}, room = room)

@socketio.on('text', namespace = '/chatroom')
def message(data):
    # username = session.get('username')
    user_id = session.get('user_id')
    room = session.get('room')
    msg = data['msg'].lstrip()
    print('{} message send to frontend'.format(msg))
    if msg != '':
        emit('message', {'user_id': user_id, 'msg': msg}, room = room)

@socketio.on('leave', namespace = '/chatroom')
def on_leave(data):
    # username = session.get('username')
    user_id = session.get('user_id')
    room = session.get('room')
    leave_room(room)
    emit('message', {'user_id': user_id, 'msg': 'has left the room.'}, room = room)

if __name__ == '__main__':
    socketio.run(app, host = '0.0.0.0', port = '5000')
	# app.run(host = '0.0.0.0', port = '5000')
