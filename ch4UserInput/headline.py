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
from flask import request

app = Flask(__name__)

RSS_FEEDS = {
             'geekpark': 'http://www.geekpark.net/rss',
             'ifanr': 'http://www.ifanr.com/feed'
             }


DEFAULTS = {'publication': 'ifanr',
            'city': 'London,UK',
            'currency_from': 'GBP',
            'currency_to': 'USD'
            }

@app.route("/")
@app.route("/<publication>")
def  home():
    publication = request.args.get('publication')
    if not publication:
        publication = DEFAULTS['publication']
    articles = get_news(publication)

    return render_template("home.html", articles=articles)

def get_news(publication):
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']



if __name__ == "__main__":
    app.run(port=5000, debug=True)
