import pytest
import os

# 1. ตั้งค่า Environment Variable ให้เป็น 'testing' **ก่อน** ที่จะ import 'app'
os.environ['FLASK_ENV'] = 'testing'

# 2. เมื่อ import มา ณ บรรทัดนี้ 'flask_app' จะเป็นแอปที่เชื่อมต่อกับ SQLite แล้ว
from app import app as flask_app, db as sqlalchemy_db


@pytest.fixture(scope='function')
def client():
    """
    สร้าง Test Client และจัดการ Application Context และฐานข้อมูล
    สำหรับแต่ละฟังก์ชันเทส
    """
    # 3. สร้าง Application Context ขึ้นมา
    with flask_app.app_context():
        # 4. สร้างตารางทั้งหมดในฐานข้อมูล SQLite in-memory ภายใน Context
        sqlalchemy_db.create_all()

        # 5. "yield" หรือส่ง test_client กลับไปให้ฟังก์ชันเทสใช้งาน
        # **จุดสำคัญคือ yield อยู่ภายใน with block**
        # ทำให้ Application Context ยังคงอยู่ตลอดการรันของฟังก์ชันเทส
        yield flask_app.test_client()

        # --- ส่วนนี้จะทำงานหลังเทสแต่ละฟังก์ชันเสร็จสิ้น ---
        
        # 6. ล้าง session และลบตารางทั้งหมดทิ้ง (ยังคงอยู่ภายใน Context)
        sqlalchemy_db.session.remove()
        sqlalchemy_db.drop_all()
