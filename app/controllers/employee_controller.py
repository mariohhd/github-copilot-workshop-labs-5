from typing import List, Dict, Optional, Union
from ..models.schemas import EmployeeCreate, EmployeeUpdate


class EmployeeController:
    def __init__(self, employee_model):
        self.employee_model = employee_model

    def list_employees(self) -> List[Dict]:
        """Get all employees"""
        return self.employee_model.get_all_employees()

    def add_employee(self, employee_data: EmployeeCreate) -> Dict:
        """Create a new employee"""
        return self.employee_model.create_employee(employee_data)

    def delete_employee(self, employee_id: Union[int, str]) -> bool:
        """Delete an employee by ID"""
        return self.employee_model.remove_employee(employee_id)

    def update_employee(self, employee_id: Union[int, str], employee_data: EmployeeUpdate) -> Optional[Dict]:
        """Update an employee by ID"""
        return self.employee_model.modify_employee(employee_id, employee_data)

    def get_employee_by_id(self, employee_id: Union[int, str]) -> Optional[Dict]:
        """Get an employee by ID"""
        return self.employee_model.get_employee_by_id(employee_id)

    def get_employee_by_email(self, email: str) -> Optional[Dict]:
        """Get an employee by email"""
        return self.employee_model.get_employee_by_email(email)

    def get_employees_by_department(self, department: str) -> List[Dict]:
        """Get employees by department"""
        return self.employee_model.get_employees_by_department(department)