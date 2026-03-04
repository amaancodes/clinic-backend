import pytest
from unittest.mock import patch
from app.departments.services import DepartmentService
from app.departments.models import Department

def test_department_service_create_success(db_session):
    dept = DepartmentService.create_department("Pediatrics")
    assert dept.id is not None
    assert dept.name == "Pediatrics"

def test_department_service_create_rollback_on_error(db_session):
    # Mock the repository to raise an exception
    with patch("app.departments.services.department_repository.create") as mock_create:
        mock_create.side_effect = Exception("DB Error")
        
        with pytest.raises(Exception, match="DB Error"):
            DepartmentService.create_department("Pediatrics")

def test_department_service_list_departments(db_session):
    DepartmentService.create_department("Pediatrics")
    DepartmentService.create_department("Orthopedics")
    
    depts = DepartmentService.list_departments()
    names = [d.name for d in depts]
    assert "Pediatrics" in names
    assert "Orthopedics" in names
