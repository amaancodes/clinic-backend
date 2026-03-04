from app.departments.models import Department
from app.core.extensions import db

class DepartmentRepository:
    def create(self, name: str) -> Department:
        dept = Department(name=name)
        db.session.add(dept)
        return dept

    def get_all(self, limit=None, offset=None) -> list[Department]:
        query = Department.query
        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)
        return query.all()

    def get_by_id(self, dept_id: int) -> Department | None:
        return db.session.get(Department, dept_id)

    def get_by_name(self, name: str) -> Department | None:
        return Department.query.filter_by(name=name).first()

department_repository = DepartmentRepository()
