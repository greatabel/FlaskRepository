from flask import Flask
import sys
import os

import site


# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('/root/.virtualenvs/env1/lib/python3.4/site-packages')

# Activate your virtual env
activate_env=os.path.expanduser("/root/.virtualenvs/env1/bin/activate_this.py")
# execfile(activate_env, dict(__file__=activate_env))
# exec(compile(open(activate_env, "r").read(), activate_env, 'exec'), dict(__file__=activate_env))
with open(activate_env) as f:
    code = compile(f.read(), activate_env, 'exec')
    exec(code, dict(__file__=activate_env))

import feedparser
app = Flask(__name__)

@app.route("/")
def index():
    return "Hello, World from Abel. " + sys.version


if __name__ == "__main__":
    app.run(port=5000, debug=True)