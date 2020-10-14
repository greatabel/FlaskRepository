from flask import Flask, request
from flask import render_template
from flask import make_response

app = Flask(__name__)
app.debug = True

@app.route('/scp2/')
@app.route('/scp2/<index_id>')
def scp2(index_id=""):
    # input :http://www.baidu.com
    query_value = request.args.get('query')
    index =  " is here"
    r = make_response(
        render_template('scp2.html', query_value=query_value,index=index)
        )
    r.headers.set('Content-Security-Policy', "default-src 'unsafe-inline' 'unsafe-eval' 'self'  ")
    return r


@app.route('/scp3/')
@app.route('/scp3/<index_id>')
def scp3(index_id=""):
    # input :http://www.baidu.com
    query_value = request.args.get('query')
    index =  " is here"
    r = make_response(
        render_template('scp3.html', query_value=query_value,index=index)
        )
    r.headers.set('Content-Security-Policy', "default-src * 'unsafe-inline'; connect-src 'self' 'nonce-987654321' ")
    return r

if __name__ == '__main__':
    app.run()