import json
from flask import (jsonify, render_template,abort,
                   request, url_for, flash, redirect, Response, send_from_directory, current_app,
                   make_response)

from datetime import datetime, timedelta
from sqlalchemy.sql import text,func
from app import app
from app import db
from app.models.project import Student, Degree, Project, FileType, Supervisor, Category, \
    ProjectSupervisor, ProjectCategory, ProjectFileType, Admin, ProjectStudent, ProjectDegree
from .schemas import ProjectSearchSchema
import jwt

@app.route('/_test_400_error')
def test_400_error():
    abort(400)
    
@app.errorhandler(400)
def bad_request_error(error):
   
    return jsonify({"error": "Bad Request"}), 400

@app.errorhandler(404)
def not_found_error(error):
    """Error handler for 404 Not Found."""
    return jsonify({"error": "Not Found"}), 404

@app.route('/')
def home():
    return "Flask says 'Hello world!'"

@app.route('/db')
def db_connection():
    try:
        with db.engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return '<h1>db works.</h1>'
    except Exception as e:
        return '<h1>db is broken.</h1>' + str(e)

@app.route('/api/set-session', methods=['POST'])
def set_session():
    """
    Endpoint นี้ถูกเรียกโดย callback.php (ระบบเก่า) [cite: 1-310]
    เพื่อรับข้อมูล User และสร้าง JWT Token ส่งกลับไป
    """
    data = request.get_json()
    if not data:
        return jsonify(error="No data provided"), 400

    cmuitaccount = data.get('cmuitaccount')
    if not cmuitaccount:
            return jsonify(error="Missing cmuitaccount"), 400

    payload = {
        'cmuitaccount': cmuitaccount,
        'firstname_TH': data.get('firstname_TH'),
        'lastname_TH': data.get('lastname_TH'),
        'organization': data.get('organization'),
        'student_id': data.get('student_id'),
        'exp': datetime.utcnow() + timedelta(minutes=15) # 👈 Token หมดอายุ 15 นาที
    }

    try:
        token = jwt.encode(
            payload,
            app.config['SECRET_KEY'], # (ดึงมาจาก __init__.py)
            algorithm="HS256"
        )
        # ส่ง Token กลับไปให้ PHP
        return jsonify(token=token)
    
    except Exception as e:
        return jsonify(error=str(e)), 500



@app.route('/api/projects', methods=['POST'])
def query_projects():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Bad Request", "messages": "Invalid JSON format."}), 400

    schema = ProjectSearchSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify({"error": "Bad Request", "messages": errors}), 400
    query = Project.query

    #filter
    if "project_name" in data:
        query = query.filter(Project.project_name == data["project_name"])
    if "year" in data:
        query = query.filter(Project.year == data["year"])
    if "students" in data:
        query = query.filter(Project.students.any(Student.stu_id.in_(data["students"])))
    if "supervisors" in data:
        query = query.filter(Project.supervisors.any(Supervisor.name.in_(data["supervisors"])))
    if "categories" in data:
        query = query.filter(Project.categories.any(Category.categoryName.in_(data["categories"])))
    if "degrees" in data:
        query = query.filter(Project.degrees.any(Degree.degree.in_(data["degrees"])))
    if "filetypes" in data:
        query = query.filter(Project.filetypes.any(FileType.file_type.in_(data["filetypes"])))

    projects = query.distinct().all()

    result = []
    for p in projects:
        result.append({
            "projectID": p.projectID,
            "project_name": p.project_name,
            "description": p.description,
            "view": p.view,
            "year": p.year,
            "expire_after": p.expire_after.isoformat() if p.expire_after else None,
            "file_path": p.file_path,
            "students": [{"stu_id": s.stu_id, "firstname": s.firstname, "lastname": s.lastname} for s in p.students],
            "degrees": [d.degree for d in p.degrees],
            "supervisors": [s.name for s in p.supervisors],
            "categories": [c.categoryName for c in p.categories],
            "filetypes": [f.file_type for f in p.filetypes],
        })

    return jsonify(result)

@app.route('/api/health')
def api_health():
    return jsonify(status='ok')


@app.route('/api/facets')
def get_facets():
    # Advisors ที่มีผูกกับโปรเจกต์
    advisors = [
        r[0] for r in db.session.query(Supervisor.name)
        .filter(Supervisor.name.isnot(None))
        .order_by(Supervisor.name.asc())
        .all()
    ]

    # หมวดหมู่ทั้งหมด
    categories = [
        r[0] for r in db.session.query(Category.categoryName)
        .filter(Category.categoryName.isnot(None))
        .order_by(Category.categoryName.asc())
        .all()
    ]

    # ประเภทไฟล์ / ประเภทผลงานทั้งหมด
    types_ = [
        r[0] for r in db.session.query(FileType.file_type)
        .filter(FileType.file_type.isnot(None))
        .order_by(FileType.file_type.asc())
        .all()
    ]

    # ระดับปริญญาทั้งหมด
    degrees = [
        r[0] for r in db.session.query(Degree.degree)
        .filter(Degree.degree.isnot(None))
        .order_by(Degree.degree.asc())
        .all()
    ]

    # ปีที่มีในตาราง Project จริง (distinct)
    years = [
        r[0] for r in db.session.query(Project.year)
        .filter(Project.year.isnot(None))
        .distinct()
        .order_by(Project.year.desc())
        .all()
    ]

    # Keywords (ใช้ชื่อโปรเจกต์ยอดวิวสูงสุดก่อน)
    keywords = [
        r[0] for r in db.session.query(Project.project_name)
        .filter(Project.project_name.isnot(None))
        .order_by(Project.view.desc().nullslast(), Project.project_name.asc())
        .limit(30)
        .all()
    ]
    min_year_scalar = db.session.query(func.min(Project.year)).scalar()
    max_year_scalar = db.session.query(func.max(Project.year)).scalar()

    default_year = datetime.now().year # fallback
    min_year = min_year_scalar if min_year_scalar is not None else default_year
    max_year = max_year_scalar if max_year_scalar is not None else default_year

    return jsonify({
        "advisors": advisors,
        "categories": categories,
        "types": types_,
        "degrees": degrees,
        "years": years,
        "keywords": keywords,
        "minYear": min_year,  # 👈 เพิ่ม
        "maxYear": max_year
    })

@app.route('/files/<path:filename>')
def uploaded_file(filename):
    # ใช้ send_from_directory เพื่อส่งไฟล์จาก path ที่เราตั้งค่าไว้ใน config
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

# ที่ด้านล่างของ views.py

@app.route('/api/all-data')
def get_all_data():
    """
    ดึงข้อมูลทั้งหมดจากตารางหลักๆ เพื่อยืนยันว่า Database และ Model ทำงานได้
    """
    try:
        # 1. ดึงข้อมูล Project ทั้งหมด
        all_projects = Project.query.all()
        projects_result = [{
            "projectID": p.projectID,
            "project_name": p.project_name,
            "year": p.year,
            "description_length": len(p.description) if p.description else 0
        } for p in all_projects]

        # 2. ดึงข้อมูล Student ทั้งหมด
        all_students = Student.query.all()
        students_result = [{
            "stu_id": s.stu_id,
            "firstname": s.firstname,
            "lastname": s.lastname,
            "email": s.email
        } for s in all_students]

        # 3. ดึงข้อมูล Supervisor ทั้งหมด
        all_supervisors = Supervisor.query.all()
        supervisors_result = [{
            "supervisorID": s.supervisorID,
            "name": s.name
        } for s in all_supervisors]

        return jsonify({
            "status": "success",
            "projects_count": len(projects_result),
            "students_count": len(students_result),
            "supervisors_count": len(supervisors_result),
            "data_preview": {
                "projects": projects_result[:10], # แสดงแค่ 10 รายการแรก
                "students": students_result[:10],
                "supervisors": supervisors_result[:10]
            }
        })

    except Exception as e:
        # หาก Query ล้มเหลว (เช่น ตารางหาย, UndefinedTable)
        return jsonify({
            "status": "error", 
            "message": "Database Query Failed", 
            "details": str(e)
        }), 500