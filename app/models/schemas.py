from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Union


class EmployeeBase(BaseModel):
    name: str = Field(..., min_length=1, description="Employee name")
    position: str = Field(..., min_length=1, description="Employee position")
    department: str = Field(..., min_length=1, description="Employee department")
    email: Optional[EmailStr] = Field(None, description="Employee email address")


class EmployeeCreate(EmployeeBase):
    id: Union[int, str] = Field(..., description="Employee ID")


class EmployeeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, description="Employee name")
    position: Optional[str] = Field(None, min_length=1, description="Employee position")
    department: Optional[str] = Field(None, min_length=1, description="Employee department")
    email: Optional[EmailStr] = Field(None, description="Employee email address")


class EmployeeResponse(EmployeeBase):
    id: Union[int, str] = Field(..., description="Employee ID")

    class Config:
        from_attributes = True


class EmployeeListResponse(BaseModel):
    employees: list[EmployeeResponse]
    total: int = Field(..., description="Total number of employees")


class MessageResponse(BaseModel):
    message: str = Field(..., description="Response message")