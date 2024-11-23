from sqlalchemy.orm import Session
from models.clinic import Clinic
from schemas.clinic import ClinicCreate, ClinicUpdate
from fastapi import HTTPException
from passlib.context import CryptContext

# 密碼加密工具
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 創建診所
def create_clinic(db: Session, clinic_data: ClinicCreate):
    hashed_password = pwd_context.hash(clinic_data.acct_pw)  # 密碼加密
    new_clinic = Clinic(**clinic_data.dict(), acct_pw=hashed_password)
    db.add(new_clinic)
    db.commit()
    db.refresh(new_clinic)
    return new_clinic

# 查詢診所 (單一)
def get_clinic_by_id(db: Session, cid: str):
    return db.query(Clinic).filter(Clinic.cid == cid).first()

# 登入功能 (驗證帳密)
def authenticate_clinic(db: Session, acct_name: str, password: str):
    clinic = db.query(Clinic).filter(Clinic.acct_name == acct_name).first()
    if not clinic or not pwd_context.verify(password, clinic.acct_pw):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return clinic

# 更新診所資料
def update_clinic(db: Session, cid: str, clinic_update: ClinicUpdate):
    clinic = get_clinic_by_id(db, cid)
    if not clinic:
        return None
    for key, value in clinic_update.dict(exclude_unset=True).items():
        if key == "acct_pw":
            value = pwd_context.hash(value)  # 更新密碼需重新加密
        setattr(clinic, key, value)
    db.commit()
    db.refresh(clinic)
    return clinic

# 查詢所有診所 (支援條件篩選)
def get_all_clinics(db: Session, city: str = None, district: str = None):
    query = db.query(Clinic)
    if city:
        query = query.filter(Clinic.city == city)
    if district:
        query = query.filter(Clinic.district == district)
    return query.all()
