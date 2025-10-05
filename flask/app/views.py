import json
from flask import (jsonify, render_template,
                   request, url_for, flash, redirect, Response)


from sqlalchemy.sql import text
from app import app
from app import db
from app.models.project import Student, Degree, Project, FileType, Supervisor, Category, \
    ProjectSupervisor, ProjectCategory, ProjectFileType, Admin, ProjectStudent, ProjectDegree

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

@app.route('/api/projects', methods=['POST'])
def query_projects():
    data = request.json or {}
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
        str(r[0]) for r in db.session.query(Project.year)
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

    return jsonify({
        "advisors": advisors,
        "categories": categories,
        "types": types_,
        "degrees": degrees,
        "years": years,
        "keywords": keywords
    })