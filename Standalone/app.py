import flask
from flask import request
import os
import signal
from subprocess import check_output

app = flask.Flask(__name__)
app.config["DEBUG"] = False

def get_pids(name):
    try:
        pids = map(int,check_output(["pidof",name]).split())
    except:
        print("no process running")
        return 0

    return pids

def shutdown_server():
    # get pid of supervisord
    self_pid = os.getpid()
    pids = get_pids("/usr/bin/python")
    for pid in pids:
      if pid != 0 and pid != self_pid:
        print("kill PID: ", pid)
        os.kill(pid, signal.SIGTERM)
    
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

@app.route('/', methods=['GET'])
def home():
    return "ok"

app.run()