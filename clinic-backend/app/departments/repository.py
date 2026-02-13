from app.departments.models import Department
from app.core.extensions import db

class DepartmentRepository:
    def create(self, name: str) -> Department:
        dept = Department(name=name)
        db.session.add(dept)
        return dept

    def get_all(self) -> list[Department]:
        return Department.query.all()

    def get_by_id(self, dept_id: int) -> Department | None:
        return db.session.get(Department, dept_id)

    def get_by_name(self, name: str) -> Department | None:
        return Department.query.filter_by(name=name).first()

department_repository = DepartmentRepository()
