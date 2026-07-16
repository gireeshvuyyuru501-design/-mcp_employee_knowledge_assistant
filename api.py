from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional

from database.connection import SessionLocal
from database import crud

app = FastAPI(
    title="Employee Knowledge API",
    version="1.0.0",
)


class EmployeeCreate(BaseModel):
    employee_id: str
    name: str
    department: str
    designation: str
    email: EmailStr


class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    department: Optional[str] = None
    designation: Optional[str] = None
    email: Optional[EmailStr] = None


@app.get("/")
def root() -> dict:
    return {
        "message": "Employee Knowledge API is running",
        "docs": "/docs",
    }


@app.get("/employees")
def list_employees() -> list[dict]:
    db = SessionLocal()
    try:
        return crud.list_employees(db)
    finally:
        db.close()


@app.get("/employees/search")
def search_employees(keyword: str) -> dict:
    db = SessionLocal()
    try:
        employees = crud.search_employees(db, keyword)
        return {
            "count": len(employees),
            "employees": employees,
        }
    finally:
        db.close()


@app.get("/employees/department/{department}")
def filter_by_department(department: str) -> dict:
    db = SessionLocal()
    try:
        employees = crud.filter_by_department(db, department)
        return {
            "department": department,
            "count": len(employees),
            "employees": employees,
        }
    finally:
        db.close()


@app.get("/employees/{employee_id}")
def get_employee(employee_id: str) -> dict:
    db = SessionLocal()
    try:
        employee = crud.get_employee_by_id(db, employee_id)

        if employee is None:
            raise HTTPException(status_code=404, detail="Employee not found")

        return employee
    finally:
        db.close()


@app.post("/employees", status_code=201)
def add_employee(payload: EmployeeCreate) -> dict:
    db = SessionLocal()
    try:
        return crud.add_employee(
            db=db,
            employee_id=payload.employee_id,
            name=payload.name,
            department=payload.department,
            designation=payload.designation,
            email=str(payload.email),
        )
    except ValueError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail=str(exc))
    finally:
        db.close()


@app.put("/employees/{employee_id}")
def update_employee(
    employee_id: str,
    payload: EmployeeUpdate,
) -> dict:
    db = SessionLocal()
    try:
        employee = crud.update_employee(
            db=db,
            employee_id=employee_id,
            name=payload.name,
            department=payload.department,
            designation=payload.designation,
            email=str(payload.email) if payload.email else None,
        )

        if employee is None:
            raise HTTPException(status_code=404, detail="Employee not found")

        return employee
    finally:
        db.close()


@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: str) -> dict:
    db = SessionLocal()
    try:
        deleted = crud.delete_employee(db, employee_id)

        if not deleted:
            raise HTTPException(status_code=404, detail="Employee not found")

        return {
            "success": True,
            "message": f"{employee_id} deleted successfully",
        }
    finally:
        db.close()


@app.get("/summary")
def employee_summary() -> dict:
    db = SessionLocal()
    try:
        return crud.employee_summary(db)
    finally:
        db.close()