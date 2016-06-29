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
from flask import make_response
import json
import urllib
import datetime


try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

app = Flask(__name__)

RSS_FEEDS = {
             'geekpark': 'http://www.geekpark.net/rss',
             'ifanr': 'http://www.ifanr.com/feed'
             }

WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID=cb932829eacb6a0e9ee4f38bfbf112ed"
CURRENCY_URL = "https://openexchangerates.org//api/latest.json?app_id=b23c94daab584f4580e4e2bf75cbcf7e"

DEFAULTS = {'publication': 'ifanr',
            'city': 'Hongkou, CN',
            'currency_from': 'CNY',
            'currency_to': 'USD'
            }

def get_value_with_fallback(key):
    if request.args.get(key):
        return request.args.get(key)
    if request.cookies.get(key):
        return request.cookies.get(key)
    return DEFAULTS[key]
    
@app.route("/")
@app.route("/<publication>")
def  home():
    # get customised headlines, based on user input or default
    publication = get_value_with_fallback("publication")
    articles = get_news(publication)

    # get customised weather based on user input or default
    city = get_value_with_fallback("city")
    weather = get_weather(city)

    # get customised currency based on user input or default
    currency_from = get_value_with_fallback("currency_from")
    currency_to = get_value_with_fallback("currency_to")
    rate, currencies = get_rate(currency_from, currency_to)

    response = make_response(
                             render_template("home.html", articles=articles, weather=weather,
                           currency_from=currency_from, currency_to=currency_to, rate=rate,
                           currencies=sorted(currencies))
                             )
    expires = datetime.datetime.now() + datetime.timedelta(days=365)
    response.set_cookie("publication", publication, expires=expires)
    response.set_cookie("city", city, expires=expires)
    response.set_cookie("currency_from", currency_from, expires=expires)
    response.set_cookie("currency_to", currency_to, expires=expires)
    return response

def get_news(publication):
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']

def  get_weather(query):
    query = urllib.parse.quote(query)
    print('query=',query)
    url = WEATHER_URL.format(query)
    print('url=',url)
    data = urllib2.urlopen(url).read()
    parsed = json.loads(data.decode())
    print('parsed=',parsed)
    if parsed.get('weather'):
        weather = {'description': parsed['weather'][0]['description'],
                   'temperature': parsed['main']['temp'],
                   'city': parsed['name'],
                   'country': parsed['sys']['country']
                   }
    return weather


def get_rate(frm, to):
    all_currency = urllib2.urlopen(CURRENCY_URL).read()
    parsed = json.loads(all_currency.decode()).get('rates')
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())
    return (to_rate / frm_rate, parsed.keys())


if __name__ == "__main__":
    app.run(port=50005, debug=True)
