from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Union
from ..controllers.employee_controller import EmployeeController
from ..models.employee import Employee
from ..models.schemas import (
    EmployeeCreate, 
    EmployeeUpdate, 
    EmployeeResponse, 
    EmployeeListResponse,
    MessageResponse
)
from app.utils.jwt import verify_token

employee_router = APIRouter(tags=["employees"])
employee_model = Employee
controller = EmployeeController(employee_model)


@employee_router.get("/employees", response_model=List[EmployeeResponse])
def list_employees(current_user: str = Depends(verify_token)):
    """Get all employees (JWT protected)"""
    employees = controller.list_employees()
    return employees


@employee_router.post("/employees", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
def add_employee(employee_data: EmployeeCreate, current_user: str = Depends(verify_token)):
    """Create a new employee (JWT protected)"""
    try:
        employee = controller.add_employee(employee_data)
        return employee
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@employee_router.delete("/employees/{employee_id}", response_model=MessageResponse)
def delete_employee(employee_id: Union[int, str]):
    """Delete an employee by ID"""
    success = controller.delete_employee(employee_id)
    if success:
        return {"message": f"Employee {employee_id} deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Employee not found")


@employee_router.get("/employees/{employee_id}", response_model=EmployeeResponse)
def get_employee_by_id(employee_id: Union[int, str]):
    """Get an employee by ID"""
    employee = controller.get_employee_by_id(employee_id)
    if employee:
        return employee
    else:
        raise HTTPException(status_code=404, detail="Employee not found")


@employee_router.get("/employees/by-email/{email}", response_model=EmployeeResponse)
def get_employee_by_email(email: str):
    """Get an employee by email"""
    employee = controller.get_employee_by_email(email)
    if employee:
        return employee
    else:
        raise HTTPException(status_code=404, detail="Employee not found")


@employee_router.put("/employees/{employee_id}", response_model=EmployeeResponse)
def update_employee(employee_id: Union[int, str], employee_data: EmployeeUpdate):
    """Update an employee by ID"""
    employee = controller.update_employee(employee_id, employee_data)
    if employee:
        return employee
    else:
        raise HTTPException(status_code=404, detail="Employee not found")


@employee_router.get("/employees/by-department/{department}", response_model=List[EmployeeResponse])
def get_employees_by_department(department: str):
    """Get employees by department"""
    employees = controller.get_employees_by_department(department)
    return employees