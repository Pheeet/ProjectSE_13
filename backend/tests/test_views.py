# backend/tests/test_views.py
import pytest
from app.models.project import Project, Category, Supervisor

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

def test_home_page(client):
    """
    ทดสอบว่าหน้า Home (/) สามารถเข้าถึงและได้ข้อมูลที่ถูกต้อง
    """
    response = client.get('/')
    assert response.status_code == 200
    assert b"Flask says 'Hello world!'" in response.data

def test_db_connection_page(client):
    """
    ทดสอบว่าหน้า /db สามารถเชื่อมต่อกับฐานข้อมูลได้สำเร็จ
    """
    response = client.get('/db')
    assert response.status_code == 200
    assert b"db works." in response.data