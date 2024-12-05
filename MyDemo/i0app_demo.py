from flask import Flask
import socket

app = Flask(__name__)

@app.route('/')
def hello():
    hostname = socket.gethostname()  # 获取主机名
    ip = socket.gethostbyname(hostname)  # 获取IP地址
    return f'Hello World from {hostname} (IP: {ip})'


if __name__ == '__main__':
    app.run(debug=True)
