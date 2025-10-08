class Employee:
    employees = []

    def __init__(self, id, name, position, department, email=None):
        self.id = id
        self.name = name
        self.position = position
        self.department = department
        self.email = email

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'position': self.position,
            'department': self.department,
            'email': self.email
        }

    @classmethod
    def create_employee(cls, employee_data):
        employee = Employee(**employee_data)
        cls.employees.append(employee)
        return employee.to_dict()

    @classmethod
    def remove_employee(cls, employee_id):
        cls.employees = [employee for employee in cls.employees if employee.id != employee_id]

    @classmethod
    def modify_employee(cls, employee_id, employee_data):
        # Improve performance of this method
        for employee in cls.employees:
            if employee.id == employee_id:
                employee.name = employee_data.get('name', employee.name)
                employee.position = employee_data.get('position', employee.position)
                employee.department = employee_data.get('department', employee.department)
                return employee.to_dict()
        return None

    @classmethod
    def get_employee_by_id(cls, employee_id):
        for employee in cls.employees:
            if employee.id == employee_id:
                return employee.to_dict()
        return None

    @classmethod
    def get_employee_by_email(cls, email):
        for employee in cls.employees:
            if employee.email == email:
                return employee.to_dict()
        return None
    
    @classmethod
    def get_all_employees(cls):
        return [employee.to_dict() for employee in cls.employees]
        