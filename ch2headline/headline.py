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

app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640'}


@app.route("/")
@app.route("/<publication>")
def get_news(publication="bbc"):
    feed = feedparser.parse(RSS_FEEDS[publication])
    first_article = feed['entries'][0]
    return """<html>
    <body>
        <h1>Headlines </h1>
        <b>{0}</b> </ br>
        <i>{1}</i> </ br>
        <p>{2}</p> </ br>
    </body>
</html>""".format(first_article.get("title"),
                  first_article.get("published"),
                  first_article.get("summary"))


if __name__ == "__main__":
    app.run(port=50099, debug=True)
