from flask.cli import FlaskGroup

from datetime import date
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
    # Students (10 คน)
    students = [
        Student(stu_id=1, firstname="สมชาย", lastname="ใจดี", email="somchai@example.com", status=True),
        Student(stu_id=2, firstname="สมหญิง", lastname="น่ารัก", email="somying@example.com", status=False),
        Student(stu_id=3, firstname="อนันต์", lastname="เก่งงาน", email="anan@example.com", status=True),
        Student(stu_id=4, firstname="กมล", lastname="ขยัน", email="kamon@example.com", status=True),
        Student(stu_id=5, firstname="พรทิพย์", lastname="สดใส", email="porntip@example.com", status=False),
        Student(stu_id=6, firstname="วิชัย", lastname="ตั้งใจ", email="wichai@example.com", status=True),
        Student(stu_id=7, firstname="จันทร์เพ็ญ", lastname="ใจดี", email="janpen@example.com", status=True),
        Student(stu_id=8, firstname="สมปอง", lastname="มุ่งมั่น", email="sompong@example.com", status=True),
        Student(stu_id=9, firstname="สุนีย์", lastname="รักเรียน", email="sunee@example.com", status=False),
        Student(stu_id=10, firstname="ปกรณ์", lastname="สร้างสรรค์", email="pakorn@example.com", status=True),
    ]
    db.session.add_all(students)

    # Degrees
    degrees = [
        Degree(degree="Bachelor"),
        Degree(degree="Master"),
        Degree(degree="PhD"),
    ]
    db.session.add_all(degrees)

    # Supervisors
    supervisors = [
        Supervisor(name="รศ.ดร. กิตติศักดิ์"),
        Supervisor(name="ผศ. ดร. พรทิพย์"),
        Supervisor(name="อ. วิชาญ"),
    ]
    db.session.add_all(supervisors)

    # Categories
    categories = [
        Category(categoryName="Artificial Intelligence"),
        Category(categoryName="Web Development"),
        Category(categoryName="Data Science"),
        Category(categoryName="Cyber Security"),
    ]
    db.session.add_all(categories)

    # FileTypes
    filetypes = [
        FileType(file_type="PDF"),
        FileType(file_type="ZIP"),
        FileType(file_type="DOCX"),
    ]
    db.session.add_all(filetypes)

    # Projects (5 โปรเจกต์)
    projects = [
        Project(
            project_name="ระบบลงทะเบียนเรียนออนไลน์", 
            description="โปรเจกต์นี้คือแพลตฟอร์มออนไลน์ที่ช่วยให้นักศึกษาสามารถลงทะเบียนเรียน ดูตารางเรียน และจัดการแผนการเรียนได้อย่างง่ายดายและมีประสิทธิภาพ ใช้งานได้ทั้งนักศึกษาและเจ้าหน้าที่ ซึ่งยอดวิวสูงแสดงให้เห็นถึงความสำคัญและประโยชน์ของระบบ",
            view=50,
            year=2025,
            expire_after=date(2026, 1, 1),
            file_path="/files/project1.pdf"
        ),
        Project(
            project_name="แพลตฟอร์มร้านค้าออนไลน์", 
            description="เป็นแพลตฟอร์มอีคอมเมิร์ซที่สมบูรณ์แบบ ช่วยให้ธุรกิจสามารถสร้างและบริหารจัดการร้านค้าออนไลน์ของตนเองได้ มีฟีเจอร์ครบครันตั้งแต่การจัดการสินค้า, ระบบตะกร้าสินค้า, ระบบชำระเงินที่ปลอดภัย ไปจนถึงการติดตามสถานะการจัดส่งสินค้า",
            view=75, 
            year=2025, 
            expire_after=date(2026, 6, 1), 
            file_path="/files/project2.zip"
        ),
        Project(project_name="ระบบแนะนำหนังสือด้วย AI", 
            description="ระบบนี้ใช้ปัญญาประดิษฐ์ (AI) ในการวิเคราะห์ความชอบและประวัติการอ่านของผู้ใช้ เพื่อแนะนำหนังสือที่ตรงกับความสนใจเฉพาะบุคคล ช่วยให้ผู้ใช้ค้นพบหนังสือและนักเขียนใหม่ๆ ได้อย่างง่ายดาย",
            view=120, 
            year=2024, 
            expire_after=date(2025, 12, 1), 
            file_path="/files/project3.docx"
        ),
        Project(project_name="ระบบวิเคราะห์ข้อมูลนักเรียน", 
            description="เครื่องมือวิเคราะห์ข้อมูลที่ออกแบบมาสำหรับสถาบันการศึกษา ช่วยประมวลผลและแสดงผลข้อมูลผลการเรียนของนักเรียนในรูปแบบที่เข้าใจง่าย ช่วยให้ครูและผู้บริหารสามารถติดตามความก้าวหน้าของนักเรียนและตัดสินใจเพื่อพัฒนากระบวนการเรียนการสอนได้ดียิ่งขึ้น",
            view=30, 
            year=2023, 
            expire_after=date(2025, 3, 1), 
            file_path="/files/project4.pdf"
        ),
        Project(project_name="ระบบตรวจสอบความปลอดภัยเครือข่าย", 
            description="โปรเจกต์นี้คือเครื่องมือสำหรับตรวจสอบและเฝ้าระวังความปลอดภัยของเครือข่าย สามารถสแกนหาช่องโหว่, ตรวจจับภัยคุกคามที่อาจเกิดขึ้น, และสร้างรายงานเพื่อช่วยให้ผู้ดูแลระบบสามารถรักษาความสมบูรณ์และความปลอดภัยของโครงสร้างพื้นฐานเครือข่ายได้อย่างมีประสิทธิภาพ",
            view=90, 
            year=2025, 
            expire_after=date(2027, 1, 1), 
            file_path="/files/project5.zip"
        ),
    ]
    db.session.add_all(projects)
    db.session.commit()

    # เชื่อม Project กับ Student
    db.session.add_all([
        ProjectStudent(projectID=1, stu_id=1),
        ProjectStudent(projectID=1, stu_id=2),
        ProjectStudent(projectID=2, stu_id=3),
        ProjectStudent(projectID=2, stu_id=4),
        ProjectStudent(projectID=3, stu_id=5),
        ProjectStudent(projectID=3, stu_id=6),
        ProjectStudent(projectID=4, stu_id=7),
        ProjectStudent(projectID=4, stu_id=8),
        ProjectStudent(projectID=5, stu_id=9),
        ProjectStudent(projectID=5, stu_id=10),
    ])

    # เชื่อม Project กับ Degree
    db.session.add_all([
        ProjectDegree(projectID=1, degreeID=1),  # Bachelor
        ProjectDegree(projectID=2, degreeID=1),
        ProjectDegree(projectID=3, degreeID=2),  # Master
        ProjectDegree(projectID=4, degreeID=2),
        ProjectDegree(projectID=5, degreeID=3),  # PhD
    ])

    # เชื่อม Project กับ Supervisor
    db.session.add_all([
        ProjectSupervisor(projectID=1, supervisorID=1),
        ProjectSupervisor(projectID=2, supervisorID=2),
        ProjectSupervisor(projectID=3, supervisorID=3),
        ProjectSupervisor(projectID=4, supervisorID=1),
        ProjectSupervisor(projectID=5, supervisorID=2),
    ])

    # เชื่อม Project กับ Category
    db.session.add_all([
        ProjectCategory(projectID=1, categoryID=2),  # Web Dev
        ProjectCategory(projectID=2, categoryID=2),
        ProjectCategory(projectID=3, categoryID=1),  # AI
        ProjectCategory(projectID=4, categoryID=3),  # Data Science
        ProjectCategory(projectID=5, categoryID=4),  # Cyber Security
    ])

    # เชื่อม Project กับ FileType
    db.session.add_all([
        ProjectFileType(projectID=1, fileID=1),  # PDF
        ProjectFileType(projectID=2, fileID=2),  # ZIP
        ProjectFileType(projectID=3, fileID=3),  # DOCX
        ProjectFileType(projectID=4, fileID=1),
        ProjectFileType(projectID=5, fileID=2),
    ])

    db.session.commit()
    print("Dummy data ถูกสร้างเรียบร้อยแล้ว")




if __name__ == "__main__":

    cli()
