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
        # MOCK students
        Student(stu_id=11, firstname="A.", lastname="Student", email="a.student@example.com", status=True),
        Student(stu_id=12, firstname="B.", lastname="Advisor", email="b.advisor@example.com", status=True),
        Student(stu_id=13, firstname="C.", lastname="Student", email="c.student@example.com", status=True),
        Student(stu_id=14, firstname="D.", lastname="Student", email="d.student@example.com", status=True),
    ]
    db.session.add_all(students)

    # --- Degrees ---
    degrees = [
        Degree(degree="Bachelor"),
        Degree(degree="Master"),
        Degree(degree="PhD"),
        # MOCK degrees (เดิมก็ครบแล้ว)
    ]
    db.session.add_all(degrees)

    # --- Supervisors / Advisors ---
    supervisors = [
        Supervisor(name="รศ.ดร. กิตติศักดิ์"),
        Supervisor(name="ผศ. ดร. พรทิพย์"),
        Supervisor(name="อ. วิชาญ"),
        # จาก MOCK facets
        Supervisor(name="Assistant Professor Dr. Ratsameetip Wita"),
        Supervisor(name="Associate Professor Dr. Jakramate Bootkrajang"),
        Supervisor(name="Assistant Professor Dr. Prakarn Unachak"),
        Supervisor(name="Dr. Sutasinee Thovuttikul"),
        Supervisor(name="Dr. Thapanapong Rukkanchanunt"),
        Supervisor(name="Associate Professor Dr. Rattasit Sukhahuta"),
        Supervisor(name="Associate Professor Dr. Ekkarat Boonchieng"),
        Supervisor(name="Assistant Professor Dr. Dussadee Praserttitipong"),
        Supervisor(name="Assistant Professor Dr. Suphakit Awiphan"),
        Supervisor(name="Assistant Professor Dr. Wijak Srisujjalertwaja"),
        Supervisor(name="Dr. Worawut Srisukkham"),
        Supervisor(name="Assistant Professor Dr. Papangkorn Inkeaw"),
        Supervisor(name="Assistant Professor Dr. Kornprom Pikulkaew"),
        Supervisor(name="Associate Professor Dr. Jeerayut Chaijaruwanich"),
        Supervisor(name="Associate Professor Dr. Chumphol Bunkhumpornpat"),
        Supervisor(name="Associate Professor Dr. Varin Chouvatut"),
        Supervisor(name="Associate Professor Dr. Wattana Jindaluang"),
        Supervisor(name="Assistant Professor Dr. Samerkae Somhom"),
        Supervisor(name="Assistant Professor Dr. Areerat Trongratsameethong"),
        Supervisor(name="Assistant Professor Dr. Matinee Kiewkanya"),
        Supervisor(name="Assistant Professor Dr. Jakarin Chawachat"),
        Supervisor(name="Assistant Professor Dr. Prapaporn Techa-Angkoon"),
        Supervisor(name="Assistant Professor Wassana Naiyapo"),
        Supervisor(name="Assistant Professor Benjamas Panyangam"),
        Supervisor(name="Noparut Vanitchanant"),
        Supervisor(name="Dr. Kamonphop Srisopha"),
        Supervisor(name="Dr. Khukrit Osathanunkul"),
        Supervisor(name="Kittipitch Kuptavanich"),
        Supervisor(name="Sitthichoke Subpaiboonkit"),
    ]
    db.session.add_all(supervisors)

    # --- Categories ---
    categories = [
        Category(categoryName="Artificial Intelligence"),
        Category(categoryName="Web Development"),
        Category(categoryName="Data Science"),
        Category(categoryName="Cyber Security"),
        # MOCK categories
        Category(categoryName="Web App"),
        Category(categoryName="Machine Learning"),
        Category(categoryName="Image Processing"),
        Category(categoryName="Games"),
        Category(categoryName="Data Classification"),
        Category(categoryName="Data Analysis"),
        Category(categoryName="Database"),
        Category(categoryName="IoT"),
        Category(categoryName="Network"),
        Category(categoryName="Windows App"),
        Category(categoryName="Security"),
        Category(categoryName="Simulation"),
        Category(categoryName="Data Warehouse"),
        Category(categoryName="Virtual Reality"),
        Category(categoryName="Other Categories"),
    ]
    db.session.add_all(categories)

    # --- FileTypes ---
    filetypes = [
        FileType(file_type="204499"),           
        FileType(file_type="Co-operative"),     
        FileType(file_type="Independent Study"),
        FileType(file_type="Thesis"),          
        FileType(file_type="Senior Project"),   
        FileType(file_type="Research Project"), 
        FileType(file_type="Prototype"),        
        FileType(file_type="Simulation"),       
        FileType(file_type="Demo"),            
        FileType(file_type="Other Type"),       
    ]
    db.session.add_all(filetypes)

    # --- Projects ---
    projects = [
        Project(
            project_name="ระบบลงทะเบียนเรียนออนไลน์", 
            description="แพลตฟอร์มออนไลน์ที่ช่วยให้นักศึกษาสามารถลงทะเบียนเรียน ดูตารางเรียน และจัดการแผนการเรียนได้อย่างง่ายดาย",
            view=50,
            year=2025,
            expire_after=date(2026,1,1),
            file_path="/files/project1.pdf"
        ),
        Project(
            project_name="แพลตฟอร์มร้านค้าออนไลน์", 
            description="แพลตฟอร์มอีคอมเมิร์ซครบวงจร",
            view=75,
            year=2025,
            expire_after=date(2026,6,1),
            file_path="/files/project2.zip"
        ),
        Project(
            project_name="ระบบแนะนำหนังสือด้วย AI", 
            description="ระบบนี้ใช้ AI วิเคราะห์ความชอบและประวัติการอ่านเพื่อแนะนำหนังสือ",
            view=120,
            year=2024,
            expire_after=date(2025,12,1),
            file_path="/files/project3.docx"
        ),
        Project(
            project_name="ระบบวิเคราะห์ข้อมูลนักเรียน", 
            description="เครื่องมือวิเคราะห์ข้อมูลสำหรับสถาบันการศึกษา",
            view=30,
            year=2023,
            expire_after=date(2025,3,1),
            file_path="/files/project4.pdf"
        ),
        Project(
            project_name="ระบบตรวจสอบความปลอดภัยเครือข่าย", 
            description="เครื่องมือตรวจสอบและเฝ้าระวังความปลอดภัยของเครือข่าย",
            view=90,
            year=2025,
            expire_after=date(2027,1,1),
            file_path="/files/project5.zip"
        ),
        # MOCK projects
        Project(
            project_name="Deep Learning for Thai NLP",
            description="ศึกษาวิธีการประมวลผลภาษาไทยด้วยโมเดลสมัยใหม่",
            view=15,
            year=2024,
            expire_after=date(2025,12,31),
            file_path="/files/mock1.pdf"
        ),
        Project(
            project_name="Computer Vision in Agriculture",
            description="ประยุกต์ใช้ CV เพื่อตรวจโรคพืชจากภาพถ่าย",
            view=25,
            year=2023,
            expire_after=date(2025,12,31),
            file_path="/files/mock2.pdf"
        ),
        Project(
            project_name="Anomaly Detection on Campus Network",
            description="วิเคราะห์ทราฟฟิกเครือข่ายเพื่อหาพฤติกรรมผิดปกติ",
            view=40,
            year=2025,
            expire_after=date(2026,12,31),
            file_path="/files/mock3.pdf"
        ),
    ]
    db.session.add_all(projects)

    # --- Admins ---
    admins = [
        Admin(role="admin", email="admin@example.com"),
        Admin(role="super_admin", email="super_admin@example.com")
    ]
    db.session.add_all(admins)
    db.session.commit()

    # --- Relation tables (sample mapping, สมจริงแต่ไม่ครบทุกอัน) ---
    db.session.add_all([
        # ProjectStudent
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
        ProjectStudent(projectID=6, stu_id=11),
        ProjectStudent(projectID=6, stu_id=12),
        ProjectStudent(projectID=7, stu_id=13),
        ProjectStudent(projectID=8, stu_id=14),
        # ProjectDegree
        ProjectDegree(projectID=1, degreeID=1),
        ProjectDegree(projectID=2, degreeID=1),
        ProjectDegree(projectID=3, degreeID=2),
        ProjectDegree(projectID=4, degreeID=2),
        ProjectDegree(projectID=5, degreeID=3),
        ProjectDegree(projectID=6, degreeID=1),
        ProjectDegree(projectID=7, degreeID=1),
        ProjectDegree(projectID=8, degreeID=2),
        # ProjectSupervisor
        ProjectSupervisor(projectID=1, supervisorID=1),
        ProjectSupervisor(projectID=2, supervisorID=2),
        ProjectSupervisor(projectID=3, supervisorID=3),
        ProjectSupervisor(projectID=4, supervisorID=1),
        ProjectSupervisor(projectID=5, supervisorID=2),
        ProjectSupervisor(projectID=6, supervisorID=3),
        ProjectSupervisor(projectID=7, supervisorID=4),
        ProjectSupervisor(projectID=8, supervisorID=5),
        # ProjectCategory
        ProjectCategory(projectID=1, categoryID=2),
        ProjectCategory(projectID=2, categoryID=2),
        ProjectCategory(projectID=3, categoryID=1),
        ProjectCategory(projectID=4, categoryID=3),
        ProjectCategory(projectID=5, categoryID=4),
        ProjectCategory(projectID=6, categoryID=2),
        ProjectCategory(projectID=7, categoryID=3),
        ProjectCategory(projectID=8, categoryID=1),
        # ProjectFileType
        ProjectFileType(projectID=1, fileID=1), 
        ProjectFileType(projectID=2, fileID=2),  
        ProjectFileType(projectID=3, fileID=2), 
        ProjectFileType(projectID=4, fileID=1), 
        ProjectFileType(projectID=5, fileID=1), 
        ProjectFileType(projectID=6, fileID=3), 
        ProjectFileType(projectID=7, fileID=4), 
        ProjectFileType(projectID=8, fileID=5),
    ])
    db.session.commit()
    print("Dummy data ถูกสร้างเรียบร้อยแล้ว")




if __name__ == "__main__":

    cli()

