from flask.cli import FlaskGroup


from app import app, db
from app.models.project import Student, Degree, Project, FileType, Supervisor, Category, \
    ProjectSupervisor, ProjectCategory, ProjectFileType, Admin, ProjectStudent, ProjectDegree


cli = FlaskGroup(app)




@cli.command("create_db")
def create_db():
    db.reflect()
    db.drop_all()
    db.create_all()
    db.session.commit()
    print("Database ถูก reset เรียบร้อยแล้ว")



@cli.command("seed_db")
def seed_db():
    """เพิ่ม dummy data สำหรับ test"""
    # ตัวอย่าง dummy student
    s1 = Student(stu_id=1, firstname="สมชาย", lastname="ทรงแบด", email="somchai@test.com", status=True)
    s2 = Student(stu_id=2, firstname="สมหญิง", lastname="สวยดี", email="somying@test.com", status=False)

    db.session.add_all([s1, s2])

    # ตัวอย่าง dummy degree
    d1 = Degree(degree="Bachelor")
    d2 = Degree(degree="Master")
    db.session.add_all([d1, d2])

    # ตัวอย่าง dummy project
    p1 = Project(project_name="Test Project 1", description="โปรเจคตัวอย่าง", view=10, year=2025)
    db.session.add(p1)

    db.session.commit()
    print("Dummy data ถูกสร้างเรียบร้อยแล้ว")




if __name__ == "__main__":
    cli()