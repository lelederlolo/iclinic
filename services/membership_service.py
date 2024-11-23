from sqlalchemy.orm import Session
from models.membership import Membership
from schemas.membership import MembershipCreate, MembershipUpdate
from fastapi import HTTPException
from passlib.context import CryptContext

# 密碼加密工具
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 創建會員
def create_membership(db: Session, membership_data: MembershipCreate):
    # 加密密碼
    hashed_password = pwd_context.hash(membership_data.acctpw)
    new_member = Membership(
        **membership_data.dict(exclude={"acctpw"}), 
        acctpw=hashed_password
    )
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_member

# 登入功能 (驗證帳密)
def authenticate_membership(db: Session, acctname: str, password: str):
    member = db.query(Membership).filter(Membership.acctname == acctname).first()
    if not member or not pwd_context.verify(password, member.acctpw):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return member

# 查詢會員 (根據 pid 或帳號名稱)
def get_membership(db: Session, pid: str = None, acctname: str = None):
    if pid:
        return db.query(Membership).filter(Membership.pid == pid).first()
    if acctname:
        return db.query(Membership).filter(Membership.acctname == acctname).first()
    return None

# 更新會員資料
def update_membership(db: Session, pid: str, membership_update: MembershipUpdate):
    member = get_membership(db, pid=pid)
    if not member:
        raise HTTPException(status_code=404, detail="Membership not found")
    for key, value in membership_update.dict(exclude_unset=True).items():
        if key == "acctpw":  # 密碼需要重新加密
            value = pwd_context.hash(value)
        setattr(member, key, value)
    db.commit()
    db.refresh(member)
    return member

# 刪除會員
def delete_membership(db: Session, pid: str):
    member = get_membership(db, pid=pid)
    if not member:
        raise HTTPException(status_code=404, detail="Membership not found")
    db.delete(member)
    db.commit()
    return member
