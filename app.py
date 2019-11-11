import os
import kkbox_api
from time import time
from algorithm import is_suit
from datetime import timedelta
from flask_socketio import SocketIO, emit, send, join_room, leave_room
from flask import Flask, request, render_template, redirect, session, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SESSION_USE_SINGER'] = True
app.config['SESSION_PERMANENT'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days = 31)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.debug = True

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
    return jsonify({'result': ('user_id' in session), 'user_id': session['user_id'], 'user_name': session['username']})

@app.route('/match')
def match():
    start = time()
    me = session.get('user_id')
    session['room'] = me
    print('matching pool: {}'.format(matching_pool))
    for user in matching_pool:
        if is_suit(user, me):
            print('user: {}, me: {}, room: {}'.format(user, me, user))
            session['room'] = user
            socketio.emit(user, {'is_match': True}, broadcast = True, namespace = '/chat')
            del matching_pool[user]
            return jsonify({'url': '/chatroom'})
        if time() - matching_pool[user] >= 300:
            del matching_pool[user]
            socketio.emit(user, {'is_match': False}, broadcast = True, namespace = '/chat')
        if time() - start >= 30: # TTL: 30s
            return jsonify({'url': '/sorry'})
    else: # not match in the pool
        print('{} join in to matching pool'.format(me))
        matching_pool[me] = time()
        return jsonify({'url': 'waiting'}) # TODO should be result: 'waiting'

@app.route('/sorry')
def sorry():
    return render_template('sorry.html')

@app.route('/bar')
def bar():
    return render_template('bar.html')

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

@socketio.on('join', namespace = '/chatroom')
def on_join(data):
    print('{} join'.format(session))
    user_id = session.get('user_id')
    room = session.get('room')
    join_room(room)
    emit('message', {'user_id': user_id, 'msg': False}, room = room)

@socketio.on('text', namespace = '/chatroom')
def message(data):
    user_id = session.get('user_id')
    room = session.get('room')
    msg = data['msg'].lstrip()
    print('{} message send to frontend'.format(msg))
    if msg != '':
        emit('message', {'user_id': user_id, 'msg': msg}, room = room)

@socketio.on('leave', namespace = '/chatroom')
def on_leave(data):
    user_id = session.get('user_id')
    room = session.get('room')
    emit('message', {'user_id': user_id, 'msg': 'Left the room.'}, room = room)
    leave_room(room)
    session['room'] = user_id
    print('{} leave room'.format(session))

if __name__ == '__main__':
    socketio.run(app, host = '0.0.0.0', port = '5000')
	# app.run(host = '0.0.0.0', port = '5000')
