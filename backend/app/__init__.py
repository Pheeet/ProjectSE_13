import os
from flask import Flask, request, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.debug import DebuggedApplication


app = Flask(__name__, static_folder='static')
app.url_map.strict_slashes = False


app.jinja_options = app.jinja_options.copy()
app.jinja_options.update({
    'trim_blocks': True,
    'lstrip_blocks': True
})


# --- START OF MODIFICATION ---

# ตรวจสอบ Environment Variable 'FLASK_ENV'
# เพื่อสลับการตั้งค่า Config ระหว่าง Development และ Testing
if os.environ.get('FLASK_ENV') == 'testing':
    # ถ้ากำลังรันเทส:
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'a-test-secret-key'
    # บังคับให้ใช้ฐานข้อมูล SQLite ใน Memory เสมอ
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
else:
    # ถ้าเป็นการรันปกติ (Development):
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = \
        '161c157cca64d2eaddd38e55b76789a5fbc78e982c543398'
    # ใช้ฐานข้อมูลจริงจาก Environment Variable
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")

# --- END OF MODIFICATION ---

app.json.ensure_ascii = False
app.config['UPLOAD_FOLDER'] = '/app/uploads'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


if app.debug and not app.testing: # เพิ่มเงื่อนไข and not app.testing
    app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)

# Creating an SQLAlchemy instance
# ณ จุดนี้ db จะถูกสร้างโดยใช้ config ที่ถูกต้องตามโหมดที่รัน
db = SQLAlchemy(app)


@app.before_request
def remove_trailing_slash():
    # Check if the path ends with a slash but is not the root "/"
    if request.path != '/' and request.path.endswith('/'):
        return redirect(request.path[:-1], code=301)


from app import views  # noqa
