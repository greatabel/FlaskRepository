from flask import Flask
from webargs import fields
from webargs.flaskparser import use_kwargs

app = Flask(__name__)


# @app.route("/<string:lang_code>/")
# @use_kwargs({'name': fields.Str(required=False,location='query'), 'name0': fields.Str(required=False,location='query')})
# def index( lang_code, **kargs):
#     print('#'*10, kargs)

#     return "Hello " + lang_code

# from webargs import fields
# from webargs.flaskparser import use_args

# http://127.0.0.1:5000/user/1?per_page=101
@app.route('/user/<int:uid>')
@use_kwargs({'per_page': fields.Int(missing=100)},  location="query")
def user_detail(per_page, uid):
    return ('The user page for user {uid}, '
            'showing {per_page} posts.').format(uid=uid,
                                                per_page=per_page)


if __name__ == "__main__":
    app.run()