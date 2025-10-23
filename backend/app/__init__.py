import os
# ⚠️ เช็กว่ามี jsonify และ CORS
from flask import Flask, request, redirect, session, g, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.debug import DebuggedApplication
import jwt
from datetime import datetime
from flask_cors import CORS # 👈 1. ต้องมี Import

app = Flask(__name__, static_folder='static')
app.url_map.strict_slashes = False

# ⚠️ 2. ต้องเปิดใช้งาน CORS
CORS(app, supports_credentials=True, resources={
    r"/api/*": {"origins": "http://localhost:5173"}
})

app.jinja_options = app.jinja_options.copy()
app.jinja_options.update({
    'trim_blocks': True,
    'lstrip_blocks': True
})

# --- (ส่วน Config) ---
if os.environ.get('FLASK_ENV') == 'testing':
    # ... (โค้ดส่วน testing ของคุณ) ...
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'a-test-secret-key' # Use a distinct key for testing
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # Use in-memory SQLite for tests
else:
    app.config['DEBUG'] = True
    # ใช้กุญแจลับเดียวกับระบบเก่า
    app.config['SECRET_KEY'] = \
        'fbb85abdd03a5c335593c92afc42c839bf7dcd20b36d58a90f2cd6a4bb6e7742'
    # เช็ก .env.dev ว่าใช้ 'db' เป็น host
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")

# ... (ส่วน config ที่เหลือ) ...
app.json.ensure_ascii = False
app.config['UPLOAD_FOLDER'] = '/app/uploads'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if app.debug and not app.testing:
    app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)

db = SQLAlchemy(app)

# ----------------------------------------------------
# ⚠️ 3. เช็ก Logic การเชื่อม Session
# ----------------------------------------------------
@app.before_request
def check_session_and_slash():

    # 1. Allow OPTIONS (Preflight) requests to pass through for CORS
    if request.method == 'OPTIONS':
        return

    # ⚠️ 2. ADD THIS CHECK: Allow access to the dev-login route without a token
    if request.path == '/api/dev-login':
        return # Let the dev_login() function handle it

    # --- 3. Authentication check (Original code starts here) ---
    if session.get('user_id'):
        pass # Already logged in via Flask session

    else:
        token = request.cookies.get('jwt_token')
        login_url = 'https://localhost/login.php' # Correct login URL

        if not token:
            # No token found
            if request.path.startswith('/api/'):
                 # It's an API call, return 401 JSON
                return jsonify(error="Authentication required", login_url=login_url), 401
            else:
                 # It's a direct page access, redirect to login
                return redirect(login_url)

        # --- (Rest of the token decoding logic remains the same) ---
        try:
            payload = jwt.decode(
                token,
                app.config['SECRET_KEY'],
                algorithms=["HS256"]
            )
            user_identity = payload.get('cmuitaccount')
            if user_identity:
                session['user_id'] = user_identity
            else:
                # Invalid payload in token
                if request.path.startswith('/api/'):
                    return jsonify(error="Invalid token payload", login_url=login_url), 401
                else:
                    return redirect(login_url)
        except jwt.ExpiredSignatureError:
            # Token expired
            if request.path.startswith('/api/'):
                return jsonify(error="Token expired", login_url=login_url), 401
            else:
                return redirect(login_url)
        except jwt.InvalidTokenError:
            # Invalid token signature
            if request.path.startswith('/api/'):
                return jsonify(error="Invalid token", login_url=login_url), 401
            else:
                return redirect(login_url)

    # --- 4. Trailing Slash Removal (Original code) ---
    if request.path != '/' and request.path.endswith('/'):
        return redirect(request.path[:-1], code=301)


from app import views  # noqa