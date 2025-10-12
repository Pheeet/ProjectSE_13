from app import db
from sqlalchemy_serializer import SerializerMixin

class Student(db.Model, SerializerMixin):
    __tablename__ = "student"
    stu_id     = db.Column('stu_id', db.Integer, primary_key=True)
    firstname  = db.Column('firstname', db.String(255), nullable=False)
    lastname   = db.Column('lastname', db.String(255), nullable=False)
    email      = db.Column('email', db.String(255), nullable=False)
    status     = db.Column('status', db.Boolean, default=False)

class Degree(db.Model, SerializerMixin):
    __tablename__ = "degree"
    degreeID = db.Column('degreeid', db.Integer, primary_key=True, autoincrement=True)
    degree   = db.Column('degree', db.String(100), nullable=False)

class Project(db.Model, SerializerMixin):
    __tablename__ = "project"
    projectID   = db.Column('projectid', db.Integer, primary_key=True, autoincrement=True)
    project_name = db.Column('project_name', db.String(200), nullable=False)
    description = db.Column('description', db.Text)
    view         = db.Column('view', db.Integer, default=0)
    expire_after = db.Column('expire_after', db.Date)
    year         = db.Column('year', db.Integer)
    file_path    = db.Column('file_path', db.String(100))

    # relationships (ใช้ชื่อตาราง association ตามที่ SQL มี)
    students    = db.relationship('Student', secondary='project_student', backref='projects')
    supervisors = db.relationship('Supervisor', secondary='project_supervisor', backref='projects')
    categories  = db.relationship('Category', secondary='project_category', backref='projects')
    filetypes   = db.relationship('FileType',  secondary='project_filetype', backref='projects')
    degrees     = db.relationship("Degree", secondary="project_degree", backref="projects")

class FileType(db.Model, SerializerMixin):
    __tablename__ = "file_type"   # แปลงจาก file_Type -> file_type
    fileID    = db.Column('fileid', db.Integer, primary_key=True, autoincrement=True)
    file_type = db.Column('file_type', db.String(50), nullable=False)

class Supervisor(db.Model, SerializerMixin):
    __tablename__ = "supervisor"
    supervisorID = db.Column('supervisorid', db.Integer, primary_key=True, autoincrement=True)
    name         = db.Column('name', db.String(100), nullable=False)

class Category(db.Model, SerializerMixin):
    __tablename__ = "category"
    categoryID   = db.Column('categoryid', db.Integer, primary_key=True, autoincrement=True)
    categoryName = db.Column('categoryname', db.String(100), nullable=False)

class ProjectSupervisor(db.Model, SerializerMixin):
    __tablename__ = "project_supervisor"
    projectID    = db.Column('projectid', db.Integer, db.ForeignKey('project.projectid'), primary_key=True)
    supervisorID = db.Column('supervisorid', db.Integer, db.ForeignKey('supervisor.supervisorid'), primary_key=True)

class ProjectCategory(db.Model, SerializerMixin):
    __tablename__ = "project_category"   # ปรับชื่อเป็น lowercase & underscore
    projectID  = db.Column('projectid', db.Integer, db.ForeignKey('project.projectid'), primary_key=True)
    categoryID = db.Column('categoryid', db.Integer, db.ForeignKey('category.categoryid'), primary_key=True)

class ProjectFileType(db.Model, SerializerMixin):
    __tablename__ = "project_filetype"
    projectID = db.Column('projectid', db.Integer, db.ForeignKey('project.projectid'), primary_key=True)
    fileID    = db.Column('fileid', db.Integer, db.ForeignKey('file_type.fileid'), primary_key=True)

class Admin(db.Model, SerializerMixin):
    __tablename__ = "admin"
    id    = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    role  = db.Column('role', db.String(50))
    email = db.Column('email', db.String(100))

class ProjectStudent(db.Model, SerializerMixin):
    __tablename__ = "project_student"
    projectID = db.Column('projectid', db.Integer, db.ForeignKey('project.projectid'), primary_key=True)
    stu_id    = db.Column('stu_id', db.Integer, db.ForeignKey('student.stu_id'), primary_key=True)

class ProjectDegree(db.Model, SerializerMixin):
    __tablename__ = "project_degree"
    projectID = db.Column('projectid', db.Integer, db.ForeignKey('project.projectid'), primary_key=True)

    degreeID  = db.Column('degreeid', db.Integer, db.ForeignKey('degree.degreeid'), primary_key=True)
