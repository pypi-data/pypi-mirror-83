from flask import request, abort, jsonify, render_template
from flask_socketio import join_room, leave_room, send, emit

from greble_flow.managment.manager import FlowManager
from greble_flow.web.managment import socketio, app

flow_manager = FlowManager()


@app.route("/flow-processor/<flow_name>/", methods=["POST"])
def run_flow(flow_name):
    # flow_manager
    if not request.json:
        abort(400)

    return jsonify({"result": flow_manager.run(flow_name, request.json["data"])})


@socketio.on('connect')
def test_connect():
    print('Client connect')


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


@app.route("/socket-test/")
def socket_test(name=None):
    return render_template("socket.html", name=name)


@socketio.on("json")
def handle_json(json):
    print("received json: " + str(json))


@socketio.on("start")
def on_start(data):
    flow_name = data["flow_name"]
    room = flow_name
    data = data["data"]
    join_room(room)
    for item in flow_manager.run(flow_name, data):
        emit(
            f"{flow_name}-result", {"result": item}, room=room,
        )
    emit(
        f"{flow_name}-disconnect", {"result": item}, room=room,
    )
    leave_room(flow_name)

# @socketio.on("leave",namespace="/socket/flow-processor/")
# def on_leave(data):
#     username = data["username"]
#     room = data["room"]
#     leave_room(room)
#     send(username + " has left the room.", room=room)
