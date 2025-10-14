# backend/tests/test_views.py
import pytest
from app.models.project import Project, Category, Supervisor
from werkzeug.debug import DebuggedApplication
# =====================================================================
# ==                      INTEGRATION TESTS                          ==
# =====================================================================


# --- Integration Test: Basic Endpoint Tests ---
# กลุ่มนี้ทดสอบว่า Endpoint พื้นฐานสามารถเข้าถึงและทำงานได้ถูกต้อง
def test_health_check(client):
    """
    ทดสอบว่า API /api/health ทำงานและตอบกลับถูกต้อง
    - ส่วนที่ทดสอบร่วมกัน: Flask Routing
    """
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json['status'] == 'ok'

def test_get_facets_returns_data_from_seeded_db(client, db_session):
    """
    ทดสอบว่า API /api/facets ดึงข้อมูลจาก DB ที่มี dummy data ได้ถูกต้อง
    - ส่วนที่ทดสอบร่วมกัน: Flask Routing, SQLAlchemy Query, DB Connection
    """
    response = client.get('/api/facets')
    assert response.status_code == 200
    data = response.json
    assert isinstance(data, dict)
    assert len(data['advisors']) > 0
    assert len(data['categories']) > 0
    assert len(data['years']) > 0

def test_file_serving(client, db_session):
    """
    ทดสอบว่า API /files/<filename> สามารถส่งไฟล์ dummy กลับมาได้
    - ส่วนที่ทดสอบร่วมกัน: Flask Routing, File System Access
    """
    response = client.get('/files/mock1.pdf')
    assert response.status_code == 200
    assert response.mimetype == 'application/pdf'

def test_file_serving_not_found(client, db_session):
    """
    ทดสอบว่า API /files/<filename> คืนค่า 404 ถ้าไฟล์ไม่มีอยู่จริง
    - ส่วนที่ทดสอบร่วมกัน: Flask Routing, File System Access
    """
    response = client.get('/files/a-file-that-does-not-exist.pdf')
    assert response.status_code == 404


# --- Integration Test: Core Feature - POST /api/projects ---
# กลุ่มนี้ทดสอบ Logic หลักของแอปพลิเคชัน คือการค้นหาและ Filter ข้อมูล

def test_query_projects_with_empty_filter(client, db_session):
    """
    ทดสอบการค้นหาโดยไม่มีเงื่อนไข ควรจะได้โปรเจกต์ทั้งหมดกลับมา
    - ส่วนที่ทดสอบร่วมกัน: Flask Routing, SQLAlchemy Query, DB Connection
    """
    response = client.post('/api/projects', json={})
    assert response.status_code == 200
    projects = response.json
    assert isinstance(projects, list)
    assert len(projects) == 8 

def test_query_projects_with_year_filter(client, db_session):
    """
    ทดสอบการค้นหาด้วย 'year'
    - ส่วนที่ทดสอบร่วมกัน: Flask Routing, SQLAlchemy Filtering Logic, DB Connection
    """
    response = client.post('/api/projects', json={"year": 2025})
    assert response.status_code == 200
    projects = response.json
    assert len(projects) > 0
    for project in projects:
        assert project['year'] == 2025

def test_query_projects_with_category_filter(client, db_session):
    """
    ทดสอบการค้นหาด้วย 'categories' ซึ่งต้องมีการ Join Table
    - ส่วนที่ทดสอบร่วมกัน: Flask Routing, SQLAlchemy Filtering & Join Logic, DB Connection
    """
    response = client.post('/api/projects', json={"categories": ["Artificial Intelligence"]})
    assert response.status_code == 200
    projects = response.json
    assert len(projects) > 0
    for project in projects:
        assert "Artificial Intelligence" in project['categories']

def test_query_projects_with_multiple_filters(client, db_session):
    """
    ทดสอบการค้นหาด้วยเงื่อนไขหลายอย่างพร้อมกัน (AND)
    - ส่วนที่ทดสอบร่วมกัน: Flask Routing, Complex SQLAlchemy Filtering, DB Connection
    """
    filters = {
        "categories": ["Web Development"],
        "year": 2025
    }
    response = client.post('/api/projects', json=filters)
    assert response.status_code == 200
    projects = response.json
    assert len(projects) == 2
    for project in projects:
        assert project['year'] == 2025
        assert "Web Development" in project['categories']

def test_query_projects_with_no_results(client, db_session):
    """
    ทดสอบการค้นหาด้วยเงื่อนไขที่ไม่มีทางเจอผลลัพธ์
    - ส่วนที่ทดสอบร่วมกัน: Flask Routing, SQLAlchemy Filtering Logic, DB Connection
    """
    filters = {"year": 9999}
    response = client.post('/api/projects', json=filters)
    assert response.status_code == 200
    projects = response.json
    assert isinstance(projects, list)
    assert len(projects) == 0

def test_home_page_endpoint(client):
    """ทดสอบว่าหน้า Home (/) สามารถเข้าถึงและได้ข้อมูลที่ถูกต้อง"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Flask says 'Hello world!'" in response.data

def test_db_connection_page_endpoint(client, db_session):
    """ทดสอบว่าหน้า /db สามารถเชื่อมต่อกับฐานข้อมูลได้สำเร็จ"""
    response = client.get('/db')
    assert response.status_code == 200
    assert b"db works." in response.data

def test_app_is_wrapped_by_debugged_application_in_debug_mode(app):
    """
    [Unit Test]
    ทดสอบว่าเมื่อ app.debug = True, wsgi_app จะถูกหุ้มด้วย DebuggedApplication
    เพื่อเพิ่ม Coverage ใน __init__.py
    """
    # GIVEN: เรามี app fixture
    
    # WHEN: เราตั้งค่าให้ app อยู่ใน debug mode โดยตรง
    app.config['DEBUG'] = True
    
    # Reload the wsgi_app logic based on the new debug setting
    if app.debug:
        app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)

    # THEN: ตรวจสอบว่า wsgi_app เป็น instance ของ DebuggedApplication จริงๆ
    assert isinstance(app.wsgi_app, DebuggedApplication)

def test_trailing_slash_redirect(client):
    """
    [Unit Test]
    ทดสอบว่า @app.before_request ทำการ redirect URL ที่มี trailing slash
    ไปยัง URL ที่ไม่มี trailing slash ได้ถูกต้อง เพื่อเพิ่ม Coverage ใน __init__.py
    """
    # GIVEN: เรามี client
    
    # WHEN: เราเรียกไปที่ endpoint ที่มี trailing slash (/) ต่อท้าย
    response = client.get('/api/health/') # สังเกต / ที่เพิ่มเข้ามา

    # THEN: ตรวจสอบผลลัพธ์
    # 1. Status code ควรจะเป็น 301 MOVED PERMANENTLY
    assert response.status_code == 301
    
    # 2. Header 'Location' ควรจะชี้ไปยัง URL ที่ถูกต้อง (ไม่มี / ต่อท้าย)
    assert response.location == '/api/health'


def test_query_projects_with_supervisor_filter(client, db_session):
    """
    [Integration Test]
    ทดสอบการค้นหาโปรเจกต์ด้วย 'supervisors' โดยใช้ข้อมูลที่ไม่ซ้ำใคร
    """
    # GIVEN: สร้างข้อมูลที่ไม่น่าจะซ้ำกับ dummy data เดิม
    # 1. สร้าง Supervisor ที่มีชื่อเฉพาะสำหรับการเทสนี้
    unique_supervisor_name = "TEST_SUPERVISOR_XYZ"
    supervisor_a = Supervisor(name=unique_supervisor_name)
    supervisor_b = Supervisor(name="Another Supervisor") # สร้างเผื่อไว้
    
    db_session.add_all([supervisor_a, supervisor_b])
    db_session.commit()

    # 2. สร้าง Project ที่มีชื่อเฉพาะ
    unique_project_name = "Project for Supervisor Test"
    project_1 = Project(project_name=unique_project_name, year=2025)
    project_2 = Project(project_name="Another Project", year=2024)

    db_session.add_all([project_1, project_2])
    db_session.commit()

    # 3. เชื่อม Project เข้ากับ Supervisor
    project_1.supervisors.append(supervisor_a)
    project_2.supervisors.append(supervisor_b)
    
    db_session.commit()

    # WHEN: ส่ง POST request เพื่อค้นหาเฉพาะโปรเจกต์ของ Supervisor ที่ไม่ซ้ำใครของเรา
    response = client.post('/api/projects', json={"supervisors": [unique_supervisor_name]})

    # THEN: ตรวจสอบผลลัพธ์
    assert response.status_code == 200
    
    projects = response.json
    assert isinstance(projects, list)
    
    # ตอนนี้เรามั่นใจได้ว่าผลลัพธ์ที่ได้ควรจะมีแค่ 1 อันพอดี
    assert len(projects) == 1
    
    # ตรวจสอบว่าโปรเจกต์ที่ได้กลับมาคือโปรเจกต์ที่เราสร้างขึ้นจริงๆ
    assert projects[0]['project_name'] == unique_project_name