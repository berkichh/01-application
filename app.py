from flask import Flask
import socket
import os

app = Flask(__name__)

def get_ip():
    try:
        # Получение IP через подключение к внешнему серверу
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

@app.route('/')
def info():
    hostname = socket.gethostname()
    ip = get_ip()
    author = os.getenv("AUTHOR", "Not specified")
    return f"Hostname: {hostname}<br>IP: {ip}<br>Author: {author}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)