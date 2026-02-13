from app.core.extensions import db
from app.models.base import BaseModel

class Department(BaseModel):
    __tablename__ = "departments"

    name = db.Column(db.String(100), unique=True, nullable=False)
