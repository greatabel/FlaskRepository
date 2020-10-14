L1

use innerHTML to escape <script> </script> tags.
I invoke js function htmlEncode when form is submited, to 
change users's input tags into escaped ones.

Main function :

function htmlEncode ( str ) {
 var ele = document.createElement('span');
 ele.appendChild( document.createTextNode( str ) );
 return ele.innerHTML;
}


function htmlDecode ( str ) {
 var ele = document.createElement('span');
 ele.innerHTML = str;
 return ele.textContent;
}


L2
alter javascript in index.html,
make input tags into escaped ones, before insert message into local db.:


console.log(message);
message = message.replace(/</g, "&lt;").replace(/>/g, "&gt;");
console.log(message);


L3
chooseTab(unescape(parseInt(self.location.hash.substr(1))))
Using parseInt javascript function to prevent malicious users from modify the URL.
 If the user input #4' onerror="alert()" alt='exploited_image, 
 the parsed result will become only #4, the js injection would not work.


L4
check input whether is type that we want:
def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

timer= self.request.get('timer', 0)
# --------
if RepresentsInt(timer):
    timer = str(int(timer))
else:
    timer = 0
template_values = { 'timer' : timer }


L5 
filter next value, add logic in app.py as following:
if 'javascript' in next_input:
    next_input = next_input.replace('javascript', '')
    print(next_input)
template_values = {'next': next_input}

L6
add filter in js's function includeGadget(url) :

if (url.match(/^https?:\/\//) || !url.endsWith(".js")) {
  setInnerText(document.getElementById("log"),
      "Sorry, cannot load a URL containing js!");
  return;
}


Rules following CSP 2.0
used in flask:

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



Rules following CSP 3.0
used in flask:

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

