from flask import Flask
import sys

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello, World from Abel. " + sys.version


if __name__ == "__main__":
    app.run(port=5000, debug=True)