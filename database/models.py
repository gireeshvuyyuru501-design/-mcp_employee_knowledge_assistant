from sqlalchemy import Column, Integer, String

from database.connection import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(120), nullable=False, index=True)
    department = Column(String(100), nullable=False, index=True)
    designation = Column(String(120), nullable=False)
    email = Column(String(150), unique=True, nullable=False)