from __future__ import annotations
from mcp.server.fastmcp import FastMCP

from database.connection import SessionLocal
from database import crud
import csv
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP


# ---------------------------------------------------------
# MCP SERVER
# ---------------------------------------------------------

mcp = FastMCP("Employee Knowledge Assistant")


# ---------------------------------------------------------
# CSV CONFIGURATION
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "employees.csv"


def load_employees() -> list[dict[str, Any]]:
    """Load employee records from employees.csv."""

    if not CSV_FILE.exists():
        raise FileNotFoundError(
            f"CSV file not found: {CSV_FILE}. "
            "Place employees.csv in the same folder as server.py."
        )

    employees: list[dict[str, Any]] = []

    with CSV_FILE.open(
        mode="r",
        encoding="utf-8-sig",
        newline="",
    ) as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError("The employees.csv file has no column headers.")

        for row in reader:
            cleaned_row = {
                str(key).strip(): str(value).strip()
                for key, value in row.items()
                if key is not None
            }
            employees.append(cleaned_row)

    return employees


def normalize(value: Any) -> str:
    """Convert a value to lowercase text for matching."""

    return str(value or "").strip().lower()


# ---------------------------------------------------------
# NEW MCP TOOLS
# ---------------------------------------------------------

@mcp.tool()
def hello() -> str:
    """Simple test tool."""

    return "Hello from MCP!"


@mcp.tool()
def greet(name: str) -> str:
    """Greet a user by name."""

    cleaned_name = name.strip()

    if not cleaned_name:
        return "Please provide a valid name."

    return f"Hello {cleaned_name}!"


# ---------------------------------------------------------
# OLD CSV EMPLOYEE TOOLS
# ---------------------------------------------------------

@mcp.tool()
def list_employees() -> dict[str, Any]:
    """Return all employees from the CSV file."""

    try:
        employees = load_employees()

        return {
            "success": True,
            "count": len(employees),
            "employees": employees,
        }

    except Exception as error:
        return {
            "success": False,
            "error": str(error),
        }


@mcp.tool()
def search_employee(name: str) -> dict[str, Any]:
    """Search employees by full or partial name."""

    try:
        search_value = normalize(name)

        if not search_value:
            return {
                "success": False,
                "error": "Please provide an employee name.",
            }

        employees = load_employees()
        matches: list[dict[str, Any]] = []

        for employee in employees:
            employee_name = normalize(
                employee.get("name")
                or employee.get("Name")
                or employee.get("employee_name")
                or employee.get("Employee Name")
            )

            if search_value in employee_name:
                matches.append(employee)

        return {
            "success": True,
            "search": name,
            "count": len(matches),
            "employees": matches,
        }

    except Exception as error:
        return {
            "success": False,
            "error": str(error),
        }


@mcp.tool()
def get_employee_by_id(employee_id: str) -> dict[str, Any]:
    """Find one employee using an employee ID."""

    try:
        requested_id = normalize(employee_id)

        if not requested_id:
            return {
                "success": False,
                "error": "Please provide an employee ID.",
            }

        employees = load_employees()

        for employee in employees:
            current_id = normalize(
                employee.get("id")
                or employee.get("ID")
                or employee.get("employee_id")
                or employee.get("Employee ID")
            )

            if current_id == requested_id:
                return {
                    "success": True,
                    "employee": employee,
                }

        return {
            "success": False,
            "error": f"No employee found with ID {employee_id}.",
        }

    except Exception as error:
        return {
            "success": False,
            "error": str(error),
        }


@mcp.tool()
def search_by_department(department: str) -> dict[str, Any]:
    """Return employees belonging to a department."""

    try:
        requested_department = normalize(department)

        if not requested_department:
            return {
                "success": False,
                "error": "Please provide a department name.",
            }

        employees = load_employees()
        matches: list[dict[str, Any]] = []

        for employee in employees:
            employee_department = normalize(
                employee.get("department")
                or employee.get("Department")
            )

            if requested_department in employee_department:
                matches.append(employee)

        return {
            "success": True,
            "department": department,
            "count": len(matches),
            "employees": matches,
        }

    except Exception as error:
        return {
            "success": False,
            "error": str(error),
        }


@mcp.tool()
def employee_summary() -> dict[str, Any]:
    """Return total employees and department counts."""

    try:
        employees = load_employees()
        department_counts: dict[str, int] = {}

        for employee in employees:
            department = (
                employee.get("department")
                or employee.get("Department")
                or "Unknown"
            )

            department = str(department).strip() or "Unknown"

            department_counts[department] = (
                department_counts.get(department, 0) + 1
            )

        return {
            "success": True,
            "total_employees": len(employees),
            "department_counts": department_counts,
        }

    except Exception as error:
        return {
            "success": False,
            "error": str(error),
        }

@mcp.tool()
def list_employees() -> list[dict]:
    """Return all employees from PostgreSQL."""
    db = SessionLocal()

    try:
        return crud.list_employees(db)
    finally:
        db.close()


@mcp.tool()
def get_employee(employee_id: str) -> dict:
    """Get one employee by employee ID."""
    db = SessionLocal()

    try:
        employee = crud.get_employee_by_id(db, employee_id)

        if employee is None:
            return {
                "success": False,
                "message": f"Employee {employee_id} was not found.",
            }

        return {
            "success": True,
            "employee": employee,
        }
    finally:
        db.close()


@mcp.tool()
def search_employees(keyword: str) -> dict:
    """Search employees by name, ID, department, designation, or email."""
    db = SessionLocal()

    try:
        employees = crud.search_employees(db, keyword)

        return {
            "success": True,
            "count": len(employees),
            "employees": employees,
        }
    finally:
        db.close()


@mcp.tool()
def filter_employees_by_department(department: str) -> dict:
    """Return employees belonging to a department."""
    db = SessionLocal()

    try:
        employees = crud.filter_by_department(db, department)

        return {
            "success": True,
            "department": department,
            "count": len(employees),
            "employees": employees,
        }
    finally:
        db.close()


@mcp.tool()
def add_employee(
    employee_id: str,
    name: str,
    department: str,
    designation: str,
    email: str,
) -> dict:
    """Add a new employee to PostgreSQL."""
    db = SessionLocal()

    try:
        employee = crud.add_employee(
            db=db,
            employee_id=employee_id,
            name=name,
            department=department,
            designation=designation,
            email=email,
        )

        return {
            "success": True,
            "message": "Employee added successfully.",
            "employee": employee,
        }

    except ValueError as exc:
        db.rollback()

        return {
            "success": False,
            "message": str(exc),
        }

    except Exception as exc:
        db.rollback()

        return {
            "success": False,
            "message": f"Unable to add employee: {exc}",
        }

    finally:
        db.close()


@mcp.tool()
def update_employee(
    employee_id: str,
    name: str | None = None,
    department: str | None = None,
    designation: str | None = None,
    email: str | None = None,
) -> dict:
    """Update an existing employee."""
    db = SessionLocal()

    try:
        employee = crud.update_employee(
            db=db,
            employee_id=employee_id,
            name=name,
            department=department,
            designation=designation,
            email=email,
        )

        if employee is None:
            return {
                "success": False,
                "message": f"Employee {employee_id} was not found.",
            }

        return {
            "success": True,
            "message": "Employee updated successfully.",
            "employee": employee,
        }

    except Exception as exc:
        db.rollback()

        return {
            "success": False,
            "message": f"Unable to update employee: {exc}",
        }

    finally:
        db.close()


@mcp.tool()
def delete_employee(employee_id: str) -> dict:
    """Delete an employee by employee ID."""
    db = SessionLocal()

    try:
        deleted = crud.delete_employee(db, employee_id)

        if not deleted:
            return {
                "success": False,
                "message": f"Employee {employee_id} was not found.",
            }

        return {
            "success": True,
            "message": f"Employee {employee_id} deleted successfully.",
        }

    except Exception as exc:
        db.rollback()

        return {
            "success": False,
            "message": f"Unable to delete employee: {exc}",
        }

    finally:
        db.close()


@mcp.tool()
def employee_summary() -> dict:
    """Return employee totals grouped by department."""
    db = SessionLocal()

    try:
        return {
            "success": True,
            "summary": crud.employee_summary(db),
        }
    finally:
        db.close()
# ---------------------------------------------------------
# START MCP SERVER
# ---------------------------------------------------------

if __name__ == "__main__":
    mcp.run(transport="stdio")