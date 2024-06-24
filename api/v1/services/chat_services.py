import json
from api.v1.app import create_app, socketio

from flask import session, request, json as flask_json
from flask_socketio import send, emit, join_room, leave_room, \
    Namespace, disconnect, ConnectionRefusedError

# Create different config files for testing.
app = create_app()


@socketio.on('connect')
def on_connect(auth):
    if auth != {'foo': 'bar'}:  # pragma: no cover
        return False
    if request.args.get('fail'):
        raise ConnectionRefusedError('failed!')
    send('connected')
    send(json.dumps(request.args.to_dict(flat=False)))
    send(json.dumps({h: request.headers[h] for h in request.headers.keys()
                     if h not in ['Host', 'Content-Type', 'Content-Length']}))
    emit('dummy', to='nobody')


@socketio.on('disconnect')
def on_disconnect():
    disconnected = '/'
    setattr(socketio, 'disconnected', disconnected)


@socketio.event(namespace='/test')
def connect():
    send('connected-test')
    send(json.dumps(request.args.to_dict(flat=False)))
    send(json.dumps({h: request.headers[h] for h in request.headers.keys()
                     if h not in ['Host', 'Content-Type', 'Content-Length']}))


@socketio.on('disconnect', namespace='/test')
def on_disconnect_test():
    disconnected = '/test'
    setattr(socketio, 'disconnected', disconnected)


@socketio.on('connect', namespace='/bgtest')
def on_bgtest_connect():
    def background_task():
        socketio.emit('bgtest', namespace='/bgtest')

    socketio.start_background_task(background_task)


@socketio.event
def message(message):
    send(message)
    if message == 'test session':
        if not socketio.manage_session and 'a' in session:
            raise RuntimeError('session is being stored')
        if 'a' not in session:
            session['a'] = 'b'
        else:
            session['a'] = 'c'
    if message not in "test noackargs":
        return message


@socketio.on('json')
def on_json(data):
    send(data, json=True, broadcast=True)
    if not data.get('noackargs'):
        return data


@socketio.on('message', namespace='/test')
def on_message_test(message):
    send(message)


@socketio.on('json', namespace='/test')
def on_json_test(data):
    send(data, json=True, namespace='/test')


@socketio.on('my custom event')
def on_custom_event(data):
    emit('my custom response', data)
    if not data.get('noackargs'):
        return data


@socketio.on('other custom event')
@socketio.on('and another custom event')
def get_request_event(data):
    request_event_data = request.event
    setattr(socketio, 'request_event_data', request_event_data)
    emit('my custom response', data)


def get_request_event2(data):
    request_event_data = request.event
    setattr(socketio, 'request_event_data', request_event_data)
    emit('my custom response', data)


socketio.on_event('yet another custom event', get_request_event2)


@socketio.on('my custom namespace event', namespace='/test')
def on_custom_event_test(data):
    emit('my custom namespace response', data, namespace='/test')


def on_custom_event_test2(data):
    emit('my custom namespace response', data, namespace='/test')


socketio.on_event('yet another custom namespace event', on_custom_event_test2,
                  namespace='/test')


@socketio.on('my custom broadcast event')
def on_custom_event_broadcast(data):
    emit('my custom response', data, broadcast=True)


@socketio.on('my custom broadcast namespace event', namespace='/test')
def on_custom_event_broadcast_test(data):
    emit('my custom namespace response', data, namespace='/test',
         broadcast=True)


@socketio.on('join room')
def on_join_room(data):
    join_room(data['room'])


@socketio.on('leave room')
def on_leave_room(data):
    leave_room(data['room'])


@socketio.on('join room', namespace='/test')
def on_join_room_namespace(data):
    join_room(data['room'])


@socketio.on('leave room', namespace='/test')
def on_leave_room_namespace(data):
    leave_room(data['room'])


@socketio.on('my room event')
def on_room_event(data):
    room = data.pop('room')
    emit('my room response', data, room=room)


@socketio.on('my room namespace event', namespace='/test')
def on_room_namespace_event(data):
    room = data.pop('room')
    send('room message', room=room)


@socketio.on('bad response')
def on_bad_response():
    emit('my custom response', {'foo': socketio})


@socketio.on('bad callback')
def on_bad_callback():
    return {'foo': socketio}


@socketio.on('changing response')
def on_changing_response():
    data = {'foo': 'bar'}
    emit('my custom response', data)
    data['foo'] = 'baz'
    return data


@socketio.on('wildcard', namespace='*')
def wildcard(data):
    print('wildcard hit')
    emit('my custom response', data)


@socketio.on_error()
def error_handler(value):
    if isinstance(value, AssertionError):
        setattr(socketio, 'error_testing', True)
    else:
        raise value
    return 'error'



@socketio.on('error testing')
def raise_error(data):
    raise AssertionError()


@socketio.on_error('/test')
def error_handler_namespace(value):
    if isinstance(value, AssertionError):
        setattr(socketio, 'error_testing_namespace', True)
    else:
        raise value
    return 'error/test'


@socketio.on("error testing", namespace='/test')
def raise_error_namespace(data):
    raise AssertionError()


@socketio.on_error_default
def error_handler_default(value):
    if isinstance(value, AssertionError):
        setattr(socketio, 'error_testing_default', True)
    else:
        raise value
    return 'error/default'


@socketio.on("error testing", namespace='/unused_namespace')
def raise_error_default(data):
    raise AssertionError()


class MyNamespace(Namespace):
    def on_connect(self):
        send('connected-ns')
        send(json.dumps(request.args.to_dict(flat=False)))
        send(json.dumps(
            {h: request.headers[h] for h in request.headers.keys()
             if h not in ['Host', 'Content-Type', 'Content-Length']}))

    def on_disconnect(self):
        setattr(socketio, 'disconnected', '/ns')

    def on_message(self, message):
        send(message)
        if message == 'test session':
            session['a'] = 'b'
        if message not in "test noackargs":
            return message

    def on_json(self, data):
        send(data, json=True, broadcast=True)
        if not data.get('noackargs'):
            return data

    def on_exit(self, data):
        disconnect()

    def on_my_custom_event(self, data):
        emit('my custom response', data)
        if not data.get('noackargs'):
            return data

    def on_other_custom_event(self, data):
        global request_event_data
        request_event_data = request.event
        setattr(socketio, 'request_event_data', request_event_data)
        emit('my custom response', data)


socketio.on_namespace(MyNamespace('/ns'))
