import pytest
from unittest.mock import patch
from werkzeug.debug import DebuggedApplication
import sys
import importlib
from sqlalchemy import text

from app import db
from app.models.project import Project, Category, Supervisor, Student, Degree, FileType

# =====================================================================
# ==                      UNIT TESTS (Core App)                      ==
# =====================================================================

def test_app_in_debug_mode_when_not_testing(monkeypatch):
    """
    [Unit Test] ทดสอบว่า app อยู่ใน debug mode เมื่อ FLASK_ENV ไม่ใช่ 'testing'
    """
    monkeypatch.setenv('FLASK_ENV', 'development')
    app_module = sys.modules['app']
    importlib.reload(app_module)
    reloaded_app = app_module.app
    
    assert reloaded_app.config['DEBUG'] is True
    assert not reloaded_app.config['TESTING']
    assert isinstance(reloaded_app.wsgi_app, DebuggedApplication)

    # Cleanup: ตั้งค่ากลับเป็น testing เพื่อไม่ให้กระทบเทสอื่น
    monkeypatch.setenv('FLASK_ENV', 'testing')
    importlib.reload(app_module)

def test_trailing_slash_redirect(client):
    """[Unit Test] ทดสอบการ redirect URL ที่มี trailing slash"""
    response = client.get('/api/health/')
    assert response.status_code == 301
    assert response.location == '/api/health'

def test_404_not_found_handler(client):
    """[Unit Test] ทดสอบ error handler สำหรับ 404 Not Found"""
    response = client.get('/a-non-existent-url')
    assert response.status_code == 404
    assert response.is_json and response.json["error"] == "Not Found"

# =====================================================================
# ==                      INTEGRATION TESTS                          ==
# =====================================================================

@pytest.fixture(scope="function")
def seed_db_for_filters(client):
    """Fixture สำหรับสร้างข้อมูลที่ซับซ้อนเพื่อทดสอบ Filter ทุกรูปแบบ"""
    cat_web = Category(categoryName="Web Development")
    cat_ai = Category(categoryName="Artificial Intelligence")
    sup_a = Supervisor(name="Dr. A")
    sup_b = Supervisor(name="Prof. B")
    stu_1 = Student(stu_id=650610001, firstname="John", lastname="Doe", email="john.d@cmu.ac.th")
    deg_bs = Degree(degree="Bachelor of Science")
    ft_pdf = FileType(file_type="PDF")

    # Project 1: Web, 2025, Dr. A, John Doe, BS, PDF
    p1 = Project(project_name="Web Project 2025", year=2025)
    p1.categories.append(cat_web)
    p1.supervisors.append(sup_a)
    p1.students.append(stu_1)
    p1.degrees.append(deg_bs)
    p1.filetypes.append(ft_pdf)

    # Project 2: AI, 2025, Prof. B
    p2 = Project(project_name="AI Project 2025", year=2025)
    p2.categories.append(cat_ai)
    p2.supervisors.append(sup_b)
    
    db.session.add_all([cat_web, cat_ai, sup_a, sup_b, stu_1, deg_bs, ft_pdf, p1, p2])
    db.session.commit()

# --- Basic Endpoint Tests ---

def test_home_endpoint(client):
    """[Integration] ทดสอบ Endpoint หน้า Home (/)"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Flask says 'Hello world!'" in response.data

def test_db_connection_success(client):
    """[Integration] ทดสอบ Endpoint /db เมื่อเชื่อมต่อสำเร็จ"""
    response = client.get('/db')
    assert response.status_code == 200
    assert b"db works." in response.data


# --- API Endpoint Tests ---

def test_health_check_endpoint(client):
    """[Integration] ทดสอบ /api/health"""
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json['status'] == 'ok'

def test_get_facets_with_data(client, seed_db_for_filters):
    """[Integration] ทดสอบ /api/facets เมื่อมีข้อมูล"""
    response = client.get('/api/facets')
    assert response.status_code == 200
    data = response.json
    assert sorted(data['advisors']) == ["Dr. A", "Prof. B"]
    assert sorted(data['categories']) == ["Artificial Intelligence", "Web Development"]
    assert sorted(data['years']) == [2025]

def test_get_facets_with_empty_db(client):
    """[Integration] ทดสอบ /api/facets เมื่อ DB ว่าง"""
    response = client.get('/api/facets')
    assert response.status_code == 200
    data = response.json
    assert data['advisors'] == [] and data['categories'] == [] and data['years'] == []

def test_query_projects_with_all_new_filters(client, seed_db_for_filters):
    """[Integration] ทดสอบ /api/projects ด้วยเงื่อนไข Filter ที่เพิ่มเข้ามาใหม่ทั้งหมด"""
    filters = {
        "project_name": "Web Project 2025",
        "students": [650610001],
        "degrees": ["Bachelor of Science"],
        "filetypes": ["PDF"]
    }
    response = client.post('/api/projects', json=filters)
    assert response.status_code == 200
    projects = response.json
    assert len(projects) == 1
    assert projects[0]['project_name'] == "Web Project 2025"

# -- NEW TESTS TO COVER MISSING LINES --
def test_query_projects_with_year_only(client, seed_db_for_filters):
    """[Integration] ทดสอบ /api/projects ด้วย year filter เท่านั้น"""
    response = client.post('/api/projects', json={"year": 2025})
    assert response.status_code == 200
    assert len(response.json) == 2

def test_query_projects_with_supervisor_only(client, seed_db_for_filters):
    """[Integration] ทดสอบ /api/projects ด้วย supervisor filter เท่านั้น"""
    response = client.post('/api/projects', json={"supervisors": ["Prof. B"]})
    assert response.status_code == 200
    projects = response.json
    assert len(projects) == 1
    assert projects[0]['project_name'] == "AI Project 2025"

def test_query_projects_with_category_only(client, seed_db_for_filters):
    """[Integration] ทดสอบ /api/projects ด้วย category filter เท่านั้น"""
    response = client.post('/api/projects', json={"categories": ["Web Development"]})
    assert response.status_code == 200
    projects = response.json
    assert len(projects) == 1
    assert projects[0]['project_name'] == "Web Project 2025"
# -- END OF NEW TESTS --

def test_query_projects_with_empty_filter_returns_all(client, seed_db_for_filters):
    """[Integration] ทดสอบ /api/projects โดยไม่มีเงื่อนไข"""
    response = client.post('/api/projects', json={})
    assert response.status_code == 200
    assert len(response.json) == 2

def test_query_projects_bad_request(client):
    """[Integration] ทดสอบ /api/projects เมื่อส่ง request ที่ไม่ใช่ JSON"""
    response = client.post('/api/projects', data="not json", headers={'Content-Type': 'application/json'})
    assert response.status_code == 400
    assert response.is_json and response.json["error"] == "Bad Request"

@patch('app.views.send_from_directory')
def test_file_serving_success(mock_send_from_directory, client):
    """[Integration] ทดสอบ /files/<filename> สำเร็จ โดยการ Mock"""
    mock_send_from_directory.return_value = "file content"
    response = client.get('/files/somefile.pdf')
    assert response.status_code == 200
    assert response.data == b"file content"
    mock_send_from_directory.assert_called_once()

def test_file_serving_not_found(client):
    """[Integration] ทดสอบ /files/<filename> เมื่อไฟล์ไม่มีอยู่จริง"""
    response = client.get('/files/non_existent_file.pdf')
    assert response.status_code == 404

def test_db_connection_failure(client):
    """[Integration] ทดสอบ Endpoint /db เมื่อเชื่อมต่อล้มเหลว"""
    # แก้ไข: เปลี่ยนเป้าหมายการ patch ให้เจาะจงไปที่ object ที่ถูกใช้ใน view ('app.views.db')
    with patch('app.views.db.engine.connect') as mock_connect:
        # GIVEN: Mock ให้การ connect เกิด Exception
        mock_connect.side_effect = Exception("Connection failed")
        
        # WHEN: เรียก Endpoint /db
        response = client.get('/db')
        
        # THEN: ตรวจสอบว่าได้รับหน้า Error ที่ถูกต้อง
        assert response.status_code == 200
        assert b"db is broken." in response.data
        assert b"Connection failed" in response.data