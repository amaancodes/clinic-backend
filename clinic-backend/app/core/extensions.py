from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.dialects.postgresql import ExcludeConstraint

@compiles(ExcludeConstraint, 'sqlite')
def skip_exclude_constraint(element, compiler, **kw):
    return "CHECK (1=1)"

db = SQLAlchemy()

jwt = JWTManager()
