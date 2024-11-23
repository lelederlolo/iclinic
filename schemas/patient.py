from pydantic import BaseModel
from datetime import date

class PatientBase(BaseModel):
    pname: str
    birthdate: date
    gender: str
    status: str

class PatientCreate(PatientBase):
    pid: str  # 需要額外的欄位

class PatientUpdate(BaseModel):
    pname: str = None
    birthdate: date = None
    gender: str = None
    status: str = None