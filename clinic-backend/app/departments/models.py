from app.core.extensions import db
from app.models.base import BaseModel

class Department(BaseModel):
    __tablename__ = "departments"

    name = db.Column(db.String(100), unique=True, nullable=False)

    doctors = db.relationship("Doctor", secondary="doctor_departments", back_populates="departments")

    def __repr__(self):
        return f"<Department {self.id} - {self.name}>"
