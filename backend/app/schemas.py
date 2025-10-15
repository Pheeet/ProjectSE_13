# backend/app/schemas.py
from marshmallow import Schema, fields

class ProjectSearchSchema(Schema):
    """
    Schema สำหรับตรวจสอบข้อมูลขาเข้าของ Endpoint /api/projects
    """
    project_name = fields.Str(required=False)
    year = fields.Int(required=False)
    
    # กำหนดว่า fields เหล่านี้ต้องเป็น List และข้างในต้องเป็นชนิดข้อมูลที่ถูกต้อง
    students = fields.List(fields.Int(), required=False)
    supervisors = fields.List(fields.Str(), required=False)
    categories = fields.List(fields.Str(), required=False)
    degrees = fields.List(fields.Str(), required=False)
    filetypes = fields.List(fields.Str(), required=False)