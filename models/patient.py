from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Date, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class Patient(Base):
    __tablename__ = "patient"  # 映射到已存在的表
    pid = Column(String(10), primary_key=True)
    pname = Column(String(10), nullable=False)
    birthdate = Column(Date, nullable=False)
    gender = Column(String(1), nullable=False)
    status = Column(String(1), nullable=False)

    # 關聯 Membership
    membership = relationship("Membership", back_populates="patient", uselist=False)


