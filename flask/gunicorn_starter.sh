#!/bin/sh
set -e

# ถ้าอยู่ใน environment development
if [ "$APP_ENV" = "development" ]; then

  # ตรวจสอบว่า netcat ติดตั้งแล้วหรือยัง
  if command -v nc >/dev/null 2>&1; then
    echo -n "Waiting for the DBMS to accept connection "
    until nc -vz db "${DATABASE_PORT:-5432}"; do
      echo -n "."
      sleep 1
    done
    echo ""
  fi

  # สร้างฐานข้อมูลและ seed ถ้ามี manage.py
  if [ -f manage.py ]; then
    echo "Creating the database tables..."
    python3 manage.py create_db || true
    python3 manage.py seed_db || true
  fi

  # ถ้าเปิด debug ใช้ Flask development server
  if [ "$FLASK_DEBUG" = "1" ]; then
    echo "Running on Flask Development Server"
    exec python3 main.py
  fi
fi

# Production / Gunicorn
echo "Running on gunicorn"
if [ -f gunicorn.config.py ]; then
  exec gunicorn main:app -c "$PWD/gunicorn.config.py"
else
  exec gunicorn -w 2 -b 0.0.0.0:8000 main:app
fi
