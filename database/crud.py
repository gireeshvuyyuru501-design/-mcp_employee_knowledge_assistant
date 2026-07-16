from sqlalchemy import func
from sqlalchemy.orm import Session

from database.models import Employee


def list_employees(db: Session) -> list[dict]:
    employees = db.query(Employee).order_by(Employee.id).all()

    return [
        {
            "id": employee.id,
            "employee_id": employee.employee_id,
            "name": employee.name,
            "department": employee.department,
            "designation": employee.designation,
            "email": employee.email,
        }
        for employee in employees
    ]


def get_employee_by_id(db: Session, employee_id: str) -> dict | None:
    employee = (
        db.query(Employee)
        .filter(func.lower(Employee.employee_id) == employee_id.lower())
        .first()
    )

    if employee is None:
        return None

    return {
        "id": employee.id,
        "employee_id": employee.employee_id,
        "name": employee.name,
        "department": employee.department,
        "designation": employee.designation,
        "email": employee.email,
    }


def search_employees(db: Session, keyword: str) -> list[dict]:
    search_value = f"%{keyword.lower()}%"

    employees = (
        db.query(Employee)
        .filter(
            func.lower(Employee.name).like(search_value)
            | func.lower(Employee.employee_id).like(search_value)
            | func.lower(Employee.department).like(search_value)
            | func.lower(Employee.designation).like(search_value)
            | func.lower(Employee.email).like(search_value)
        )
        .order_by(Employee.id)
        .all()
    )

    return [
        {
            "id": employee.id,
            "employee_id": employee.employee_id,
            "name": employee.name,
            "department": employee.department,
            "designation": employee.designation,
            "email": employee.email,
        }
        for employee in employees
    ]


def filter_by_department(db: Session, department: str) -> list[dict]:
    employees = (
        db.query(Employee)
        .filter(func.lower(Employee.department) == department.lower())
        .order_by(Employee.name)
        .all()
    )

    return [
        {
            "id": employee.id,
            "employee_id": employee.employee_id,
            "name": employee.name,
            "department": employee.department,
            "designation": employee.designation,
            "email": employee.email,
        }
        for employee in employees
    ]


def add_employee(
    db: Session,
    employee_id: str,
    name: str,
    department: str,
    designation: str,
    email: str,
) -> dict:
    existing = (
        db.query(Employee)
        .filter(
            (func.lower(Employee.employee_id) == employee_id.lower())
            | (func.lower(Employee.email) == email.lower())
        )
        .first()
    )

    if existing:
        raise ValueError("Employee ID or email already exists.")

    employee = Employee(
        employee_id=employee_id,
        name=name,
        department=department,
        designation=designation,
        email=email,
    )

    db.add(employee)
    db.commit()
    db.refresh(employee)

    return {
        "id": employee.id,
        "employee_id": employee.employee_id,
        "name": employee.name,
        "department": employee.department,
        "designation": employee.designation,
        "email": employee.email,
    }


def update_employee(
    db: Session,
    employee_id: str,
    name: str | None = None,
    department: str | None = None,
    designation: str | None = None,
    email: str | None = None,
) -> dict | None:
    employee = (
        db.query(Employee)
        .filter(func.lower(Employee.employee_id) == employee_id.lower())
        .first()
    )

    if employee is None:
        return None

    if name is not None:
        employee.name = name
    if department is not None:
        employee.department = department
    if designation is not None:
        employee.designation = designation
    if email is not None:
        employee.email = email

    db.commit()
    db.refresh(employee)

    return {
        "id": employee.id,
        "employee_id": employee.employee_id,
        "name": employee.name,
        "department": employee.department,
        "designation": employee.designation,
        "email": employee.email,
    }


def delete_employee(db: Session, employee_id: str) -> bool:
    employee = (
        db.query(Employee)
        .filter(func.lower(Employee.employee_id) == employee_id.lower())
        .first()
    )

    if employee is None:
        return False

    db.delete(employee)
    db.commit()

    return True


def employee_summary(db: Session) -> dict:
    total_employees = db.query(Employee).count()

    department_counts = (
        db.query(Employee.department, func.count(Employee.id))
        .group_by(Employee.department)
        .order_by(Employee.department)
        .all()
    )

    return {
        "total_employees": total_employees,
        "employees_by_department": {
            department: count for department, count in department_counts
        },
    }