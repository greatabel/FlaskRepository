import sys
import os
import site

# if is on ecs server 
if sys.platform == 'linux':
    # Add the site-packages of the chosen virtualenv to work with
    site.addsitedir('/var/www/env1/lib/python3.4/site-packages')
    # Activate your virtual env
    activate_env=os.path.expanduser("/var/www/env1/bin/activate_this.py")
    with open(activate_env) as f:
        code = compile(f.read(), activate_env, 'exec')
        exec(code, dict(__file__=activate_env))
#---------------------------------------------------

import feedparser
from flask import Flask
from flask import render_template

app = Flask(__name__)

RSS_FEEDS = {
             'geekpark': 'http://www.geekpark.net/rss',
             'ifanr': 'http://www.ifanr.com/feed'
             }


@app.route("/")
@app.route("/<publication>")
def get_news(publication="ifanr"):

    feed = feedparser.parse(RSS_FEEDS[publication])
    return render_template("home.html", articles=feed['entries'])



if __name__ == "__main__":
    app.run(port=5000, debug=True)
