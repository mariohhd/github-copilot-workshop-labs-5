import re
from typing import Optional, Union, Dict, List
from .schemas import EmployeeCreate, EmployeeUpdate, EmployeeResponse


class Employee:
    employees = []

    def __init__(self, id: Union[int, str], name: str, position: str, department: str, email: Optional[str] = None):
        self.id = id
        self.name = name
        self.position = position
        self.department = department
        self.email = email

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'name': self.name,
            'position': self.position,
            'department': self.department,
            'email': self.email
        }

    @classmethod
    def create_employee(cls, employee_data: EmployeeCreate) -> Dict:
        # Check for duplicate employee ID
        if any(emp.id == employee_data.id for emp in cls.employees):
            raise ValueError(f"Employee with ID {employee_data.id} already exists")

        # Create employee from Pydantic model
        employee = Employee(
            id=employee_data.id,
            name=employee_data.name,
            position=employee_data.position,
            department=employee_data.department,
            email=employee_data.email
        )
        cls.employees.append(employee)
        return employee.to_dict()

    @classmethod
    def remove_employee(cls, employee_id: Union[int, str]) -> bool:
        initial_count = len(cls.employees)
        cls.employees = [employee for employee in cls.employees if employee.id != employee_id]
        return len(cls.employees) < initial_count

    @classmethod
    def modify_employee(cls, employee_id: Union[int, str], employee_data: EmployeeUpdate) -> Optional[Dict]:
        # Find employee by ID
        employee = None
        for emp in cls.employees:
            if emp.id == employee_id:
                employee = emp
                break
        
        if employee:
            # Update only provided fields
            if employee_data.name is not None:
                employee.name = employee_data.name
            if employee_data.position is not None:
                employee.position = employee_data.position
            if employee_data.department is not None:
                employee.department = employee_data.department
            if employee_data.email is not None:
                employee.email = employee_data.email
            return employee.to_dict()
        return None

    @classmethod
    def get_employee_by_id(cls, employee_id: Union[int, str]) -> Optional[Dict]:
        for employee in cls.employees:
            if employee.id == employee_id:
                return employee.to_dict()
        return None

    @classmethod
    def get_employee_by_email(cls, email: str) -> Optional[Dict]:
        for employee in cls.employees:
            if employee.email == email:
                return employee.to_dict()
        return None

    @classmethod
    def get_all_employees(cls) -> List[Dict]:
        return [employee.to_dict() for employee in cls.employees]

    @classmethod
    def get_employees_by_department(cls, department: str) -> List[Dict]:
        return [employee.to_dict() for employee in cls.employees if employee.department == department]
