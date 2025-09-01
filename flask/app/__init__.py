import os
from flask import Flask, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, static_folder='static')
app.url_map.strict_slashes = False


app.jinja_options = app.jinja_options.copy()
app.jinja_options.update({
    'trim_blocks': True,
    'lstrip_blocks': True
})


app.config['DEBUG'] = True
app.config['SECRET_KEY'] = \
    '161c157cca64d2eaddd38e55b76789a5fbc78e982c543398'
app.config['JSON_AS_ASCII'] = False


app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite://")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Creating an SQLAlchemy instance
db = SQLAlchemy(app)


@app.before_request
def remove_trailing_slash():
   # Check if the path ends with a slash but is not the root "/"
    if request.path != '/' and request.path.endswith('/'):
        return redirect(request.path[:-1], code=301)


from app import views  # noqa
