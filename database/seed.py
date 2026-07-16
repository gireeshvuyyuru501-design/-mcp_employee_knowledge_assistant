from database.connection import Base, SessionLocal, engine
from database.models import Employee


def seed_database() -> None:
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        existing_count = db.query(Employee).count()

        if existing_count > 0:
            print(f"Database already contains {existing_count} employees.")
            return

        employees = [
            Employee(
                employee_id="EMP001",
                name="John Smith",
                department="Engineering",
                designation="Software Engineer",
                email="john.smith@example.com",
            ),
            Employee(
                employee_id="EMP002",
                name="Sarah Johnson",
                department="Human Resources",
                designation="HR Manager",
                email="sarah.johnson@example.com",
            ),
            Employee(
                employee_id="EMP003",
                name="Michael Brown",
                department="Finance",
                designation="Financial Analyst",
                email="michael.brown@example.com",
            ),
        ]

        db.add_all(employees)
        db.commit()

        print("Database seeded successfully.")

    except Exception as exc:
        db.rollback()
        print(f"Database seed failed: {exc}")
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()