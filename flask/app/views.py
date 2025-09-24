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


    
