from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Date, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class Membership(Base):
    __tablename__ = "membership"
    pid = Column(String(10), ForeignKey("patient.pid"), primary_key=True)
    acctname = Column(String(20), unique=True, nullable=False)
    acctpw = Column(String(30), nullable=False)
    email = Column(String(30), unique=True, nullable=False)

    # 反向關聯 Patient
    patient = relationship("Patient", back_populates="membership")