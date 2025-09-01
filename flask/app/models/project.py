from app import db
from sqlalchemy_serializer import SerializerMixin

class Student(db.Model, SerializerMixin):
    __tablename__ = "student"
    stu_id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(255), nullable=False)
    lastname = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Boolean, default=False)

class Degree(db.Model, SerializerMixin):
    __tablename__ = "degree"
    degreeID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    degree = db.Column(db.String(100), nullable=False)

class Project(db.Model, SerializerMixin):
    __tablename__ = "project"
    projectID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    view = db.Column(db.Integer, default=0)
    expire_after = db.Column(db.Date)
    year = db.Column(db.Integer)
    file_path = db.Column(db.String(100))

class FileType(db.Model, SerializerMixin):
    __tablename__ = "file_Type"
    fileID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    file_type = db.Column(db.String(50), nullable=False)

class Supervisor(db.Model, SerializerMixin):
    __tablename__ = "supervisor"
    supervisorID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)

class Category(db.Model, SerializerMixin):
    __tablename__ = "category"
    categoryID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    categoryName = db.Column(db.String(100), nullable=False)

class ProjectSupervisor(db.Model, SerializerMixin):
    __tablename__ = "project_supervisor"
    projectID = db.Column(db.Integer, db.ForeignKey("project.projectID"), primary_key=True)
    supervisorID = db.Column(db.Integer, db.ForeignKey("supervisor.supervisorID"), primary_key=True)

class ProjectCategory(db.Model, SerializerMixin):
    __tablename__ = "Project_Category"
    projectID = db.Column(db.Integer, db.ForeignKey("project.projectID"), primary_key=True)
    categoryID = db.Column(db.Integer, db.ForeignKey("category.categoryID"), primary_key=True)

class ProjectFileType(db.Model, SerializerMixin):
    __tablename__ = "project_FileType"
    projectID = db.Column(db.Integer, db.ForeignKey("project.projectID"), primary_key=True)
    fileID = db.Column(db.Integer, db.ForeignKey("file_Type.fileID"), primary_key=True)

class Admin(db.Model, SerializerMixin):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role = db.Column(db.String(50))
    email = db.Column(db.String(100))

class ProjectStudent(db.Model, SerializerMixin):
    __tablename__ = "project_student"
    projectID = db.Column(db.Integer, db.ForeignKey("project.projectID"), primary_key=True)
    stu_id = db.Column(db.Integer, db.ForeignKey("student.stu_id"), primary_key=True)

class ProjectDegree(db.Model, SerializerMixin):
    __tablename__ = "project_degree"
    projectID = db.Column(db.Integer, db.ForeignKey("project.projectID"), primary_key=True)
    degreeID = db.Column(db.Integer, db.ForeignKey("degree.degreeID"), primary_key=True)