import flask
from flask_socketio import join_room, rooms

def wrap(socketio):
    @socketio.on('disconnect')
    def socket_disconnect_handler():
        for room in rooms():
            socketio.emit('peer-disconnection', {'sid': flask.request.sid}, room=room, include_self=False)

    @socketio.on('request-sid')
    def socket_request_sid(data):
        sid = flask.request.sid
        socketio.emit('sid', {'sid': sid}, room=sid)

    @socketio.on('join')
    def socket_join_room_handler(data):
        join_room(data['room'])
        socketio.emit('acquire-peers', {'sid': flask.request.sid, 'prevSid': data.get('prevSid')}, room=data['room'], include_self=False)

    @socketio.on('acquire-peers-response')
    def socket_acquire_peers_response_handler(data):
        room = data['room']
        recipient = data['recipient']
        socketio.emit('acquire-peers-response', {'sid': flask.request.sid, 'prevSid': data.get('prevSid')}, room=recipient)

    @socketio.on('offer')
    def socket_send_offer_handler(data):
        socketio.emit('offer', {'sid': flask.request.sid, **data}, room=data['recipient'])

    @socketio.on('answer')
    def socket_send_answer_handler(data):
        socketio.emit('answer', {'sid': flask.request.sid, **data}, room=data['recipient'])

    @socketio.on('candidate')
    def socket_send_candidate_handler(data):
        socketio.emit('candidate', {'sid': flask.request.sid, **data}, room=data['recipient'])