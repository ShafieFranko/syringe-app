from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class NursingRequest(Base):
    __tablename__ = "nursing_requests"

    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String, index=True)
    service_type = Column(String)
    address = Column(String)
    phone = Column(String)
    status = Column(String, default="Pending")
    assigned_nurse = Column(String, default="")
    rating = Column(String, default="")

class Nurse(Base):
    __tablename__ = "nurses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    syndicate_id = Column(String, unique=True, index=True)
    phone = Column(String)
    area = Column(String)
    is_verified = Column(Boolean, default=True)