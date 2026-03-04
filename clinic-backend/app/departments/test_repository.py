import pytest
from app.departments.repository import department_repository
from app.departments.models import Department

def test_department_repository_create(db_session):
    dept = department_repository.create("Cardiology")
    db_session.flush() # ensure id is generated
    
    assert dept.id is not None
    assert dept.name == "Cardiology"

def test_department_repository_get_all(db_session):
    department_repository.create("Cardiology")
    department_repository.create("Neurology")
    db_session.flush()
    
    depts = department_repository.get_all()
    assert len(depts) >= 2
    names = [d.name for d in depts]
    assert "Cardiology" in names
    assert "Neurology" in names

def test_department_repository_get_by_id(db_session):
    dept = department_repository.create("Cardiology")
    db_session.flush()
    
    fetched = department_repository.get_by_id(dept.id)
    assert fetched is not None
    assert fetched.id == dept.id
    assert fetched.name == "Cardiology"

def test_department_repository_get_by_name(db_session):
    department_repository.create("Cardiology")
    db_session.flush()
    
    fetched = department_repository.get_by_name("Cardiology")
    assert fetched is not None
    assert fetched.name == "Cardiology"
