import socketio

sio = socketio.Client()

sio.connect('http://localhost:3000')
