from sqlalchemy.orm import Session
from models.patient import Patient
from schemas.patient import PatientCreate, PatientUpdate
from fastapi import HTTPException

# 新增病患
def create_patient(db: Session, patient_data: PatientCreate):
    new_patient = Patient(**patient_data.dict())
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient

# 查詢病患 (根據 PID 或其他條件)
def get_patient(db: Session, pid: str = None, pname: str = None):
    if pid:
        return db.query(Patient).filter(Patient.pid == pid).first()
    if pname:
        return db.query(Patient).filter(Patient.pname == pname).all()
    raise HTTPException(status_code=400, detail="Invalid query parameters")

# 更新病患資料
def update_patient(db: Session, pid: str, patient_update: PatientUpdate):
    patient = get_patient(db, pid=pid)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    for key, value in patient_update.dict(exclude_unset=True).items():
        setattr(patient, key, value)
    db.commit()
    db.refresh(patient)
    return patient

# 刪除病患
def delete_patient(db: Session, pid: str):
    patient = get_patient(db, pid=pid)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    db.delete(patient)
    db.commit()
    return patient