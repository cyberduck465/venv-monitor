from flask import Flask, render_template
from flask_socketio import SocketIO
import os, socket, pty, subprocess

app = Flask(__name__)
socketio = SocketIO(app)

USERNAME = os.environ.get("USER") or "unknown"
HOSTNAME = socket.gethostname()
HOME_DIR = os.path.expanduser("~")

@app.route("/")
def index():
    return render_template("index.html", os_user=USERNAME, os_host=HOSTNAME, home_dir=HOME_DIR)

@socketio.on("terminal")
def terminal(ws_msg):
    # 啟動 bash 並在家目錄
    proc = subprocess.Popen(
        ["/bin/bash"],
        cwd=HOME_DIR,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    # 寫入命令
    proc.stdin.write(ws_msg + "\n")
    proc.stdin.flush()
    # 讀取輸出
    output = proc.stdout.read()
    socketio.emit("terminal_response", output)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=10000)

