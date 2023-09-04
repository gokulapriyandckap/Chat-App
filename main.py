from  Website import create_app
from flask import Flask,render_template
from flask_socketio import SocketIO, send

socketapp = Flask(__name__)
socketapp.config['SECRET'] = "secret@123"

socketio = SocketIO(socketapp, cors_allowed_origin="*")

@socketio.on('message')
def handle_message(message):
    print("received message:" + message)
    if message != "User connected!":
        send(message, broadcast=True)


@socketapp.route('/')
def index():
    return render_template("Website/templates/home.html")

app = create_app()
socketapp = create_app()
if __name__ == '__main__':
    socketio.run(socketapp,port=8000)
    app.run(debug=False,host='192.168.1.47')