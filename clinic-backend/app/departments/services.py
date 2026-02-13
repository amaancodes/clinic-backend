from app.departments.models import Department
from app.departments.repository import department_repository
from app.core.extensions import db

class DepartmentService:
    @staticmethod
    def create_department(name: str) -> Department:
        try:
            dept = department_repository.create(name)
            db.session.commit()
            return dept
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def list_departments() -> list[Department]:
        return department_repository.get_all()
