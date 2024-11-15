class Employee:
    def __init__(self, employee_id, name, department, location):
        self.employee_id = employee_id
        self.name = name
        self.department = department
        self.location = location

    def to_dict(self):
        return {
            "employeeId": self.employee_id,
            "name": self.name,
            "department": self.department,
            "location": self.location
        }
