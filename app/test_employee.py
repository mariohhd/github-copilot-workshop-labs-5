import pytest
from fastapi.testclient import TestClient
from app import create_app
from models.employee import Employee
from models.schemas import EmployeeCreate, EmployeeUpdate


@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Setup: Clear the employees list before each test
    Employee.employees = []
    yield
    # Teardown: Clear the employees list after each test
    Employee.employees = []


@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)


def test_create_employee():
    employee_data = EmployeeCreate(id=1, name='John Doe', position='Developer', department='Engineering')
    created_employee = Employee.create_employee(employee_data)
    expected_dict = {'id': 1, 'name': 'John Doe', 'position': 'Developer', 'department': 'Engineering', 'email': None}
    assert created_employee == expected_dict
    assert len(Employee.employees) == 1
    assert Employee.employees[0].to_dict() == expected_dict


def test_remove_employee():
    employee_data = EmployeeCreate(id=1, name='John Doe', position='Developer', department='Engineering')
    Employee.create_employee(employee_data)
    result = Employee.remove_employee(1)
    assert result == True
    assert len(Employee.employees) == 0


def test_modify_employee():
    employee_data = EmployeeCreate(id=1, name='John Doe', position='Developer', department='Engineering')
    Employee.create_employee(employee_data)
    updated_data = EmployeeUpdate(name='Jane Doe', position='Senior Developer')
    modified_employee = Employee.modify_employee(1, updated_data)
    assert modified_employee['name'] == 'Jane Doe'
    assert modified_employee['position'] == 'Senior Developer'
    assert modified_employee['department'] == 'Engineering'
    assert len(Employee.employees) == 1


def test_get_employee_by_id():
    employee_data = EmployeeCreate(id=1, name='John Doe', position='Developer', department='Engineering')
    Employee.create_employee(employee_data)
    employee = Employee.get_employee_by_id(1)
    expected_dict = {'id': 1, 'name': 'John Doe', 'position': 'Developer', 'department': 'Engineering', 'email': None}
    assert employee == expected_dict

    non_existent_employee = Employee.get_employee_by_id(2)
    assert non_existent_employee is None


def test_get_all_employees():
    employee_data_1 = EmployeeCreate(id=1, name='John Doe', position='Developer', department='Engineering')
    employee_data_2 = EmployeeCreate(id=2, name='Jane Doe', position='Manager', department='Sales')
    Employee.create_employee(employee_data_1)
    Employee.create_employee(employee_data_2)
    all_employees = Employee.get_all_employees()
    assert len(all_employees) == 2


def test_get_employee_by_email():
    employee_data = EmployeeCreate(id=1, name='John Doe', position='Developer', department='Engineering', email='john.doe@example.com')
    Employee.create_employee(employee_data)
    employee = Employee.get_employee_by_email('john.doe@example.com')
    expected_dict = {'id': 1, 'name': 'John Doe', 'position': 'Developer', 'department': 'Engineering', 'email': 'john.doe@example.com'}
    assert employee == expected_dict

    non_existent_employee = Employee.get_employee_by_email('jane.doe@example.com')
    assert non_existent_employee is None


# API Integration Tests

def test_api_create_employee(client):
    employee_data = {
        "id": 1,
        "name": "John Doe",
        "position": "Developer", 
        "department": "Engineering"
    }
    response = client.post("/api/v1/employees", json=employee_data)
    assert response.status_code == 201
    assert response.json()["name"] == "John Doe"


def test_api_get_all_employees(client):
    # Create test employee first
    employee_data = EmployeeCreate(id=1, name='John Doe', position='Developer', department='Engineering')
    Employee.create_employee(employee_data)
    
    response = client.get("/api/v1/employees")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_api_get_employee_by_id(client):
    # Create test employee first
    employee_data = EmployeeCreate(id=1, name='John Doe', position='Developer', department='Engineering')
    Employee.create_employee(employee_data)
    
    response = client.get("/api/v1/employees/1")
    assert response.status_code == 200
    assert response.json()["name"] == "John Doe"


def test_api_get_employee_by_id_not_found(client):
    response = client.get("/api/v1/employees/999")
    assert response.status_code == 404


def test_api_update_employee(client):
    # Create test employee first
    employee_data = EmployeeCreate(id=1, name='John Doe', position='Developer', department='Engineering')
    Employee.create_employee(employee_data)
    
    update_data = {"name": "Jane Doe", "position": "Senior Developer"}
    response = client.put("/api/v1/employees/1", json=update_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Jane Doe"


def test_api_delete_employee(client):
    # Create test employee first
    employee_data = EmployeeCreate(id=1, name='John Doe', position='Developer', department='Engineering')
    Employee.create_employee(employee_data)
    
    response = client.delete("/api/v1/employees/1")
    assert response.status_code == 200
    assert "deleted successfully" in response.json()["message"]