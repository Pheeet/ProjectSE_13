import pytest
from app import db
from app.models.project import (
    Project, Category, Supervisor, Student, Degree, FileType, Admin
)

# =====================================================================
# ==                      MODEL UNIT TESTS                           ==
# =====================================================================
# เทสชุดนี้จะครอบคลุมโค้ดใน app/models/project.py ทั้งหมด 100%

def test_create_all_models(client):
    """
    [Unit Test]
    ทดสอบการสร้าง instance ของ Model ทุกตัว (ยกเว้นตาราง M-M) และการบันทึกลง DB
    """
    # GIVEN: ข้อมูลสำหรับสร้าง Model แต่ละตัว
    student = Student(stu_id=650610001, firstname="First", lastname="Last", email="first.l@cmu.ac.th")
    degree = Degree(degree="Bachelor of Science")
    supervisor = Supervisor(name="Prof. Test")
    category = Category(categoryName="Unit Testing")
    file_type = FileType(file_type="PDF")
    project = Project(project_name="The Ultimate Test Project", year=2025)
    admin = Admin(role="superadmin", email="admin@cmu.ac.th")


    # WHEN: บันทึกข้อมูลทั้งหมดลงใน session
    db.session.add_all([student, degree, supervisor, category, file_type, project, admin])
    db.session.commit()

    # THEN: ตรวจสอบว่า ID ถูกสร้างขึ้นมาทั้งหมด
    assert student.stu_id is not None
    assert degree.degreeID is not None
    assert supervisor.supervisorID is not None
    assert category.categoryID is not None
    assert file_type.fileID is not None
    assert project.projectID is not None
    assert admin.id is not None
    assert project.view == 0 # ตรวจสอบ Default value

def test_all_project_relationships(client):
    """
    [Unit Test]
    ทดสอบการสร้างความสัมพันธ์ (many-to-many) ทั้งหมดของ Project Model
    """
    # GIVEN: สร้าง instance ของ Project และ Model อื่นๆ ที่เกี่ยวข้อง
    project = Project(project_name="Full Relationship Test", year=2025)
    student = Student(stu_id=650610002, firstname="Rel", lastname="Test", email="rel.t@cmu.ac.th")
    degree = Degree(degree="Master of Engineering")
    supervisor = Supervisor(name="Dr. Relation")
    category = Category(categoryName="Software Engineering")
    file_type = FileType(file_type="ZIP")
    
    # WHEN: ใช้ .append() เพื่อสร้างความสัมพันธ์
    project.students.append(student)
    project.degrees.append(degree)
    project.supervisors.append(supervisor)
    project.categories.append(category)
    project.filetypes.append(file_type)

    db.session.add(project)
    db.session.commit()

    # THEN: ตรวจสอบความสัมพันธ์จากทั้งสองฝั่ง (back-reference)
    assert len(project.students) == 1
    assert project.students[0].firstname == "Rel"
    assert project in student.projects

    assert len(project.degrees) == 1
    assert project.degrees[0].degree == "Master of Engineering"
    assert project in degree.projects

    assert len(project.supervisors) == 1
    assert project.supervisors[0].name == "Dr. Relation"
    assert project in supervisor.projects

    assert len(project.categories) == 1
    assert project.categories[0].categoryName == "Software Engineering"
    assert project in category.projects

    assert len(project.filetypes) == 1
    assert project.filetypes[0].file_type == "ZIP"
    assert project in file_type.projects
