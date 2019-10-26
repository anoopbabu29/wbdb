from flask import Flask, request, render_template
from flask_restful import Resource, Api
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

todos = {}

class TodoSimple(Resource):
    def get(self, todo_id):
        return {todo_id: todos[todo_id]}

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}

api.add_resource(TodoSimple, '/api/<string:todo_id>')


@app.route("/")
def index():
   return render_template("index.html")

@app.route("/other")
def other():
   return render_template("other.html")

# Recieving Messages
@socketio.on('radio')
def handle_message(message):
    print('received message: ' + str(message))
    emit('radio-receiver', message, broadcast=True)

if __name__ == '__main__':
    socketio.run(app)