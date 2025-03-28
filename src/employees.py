class Employee:
    PAYMENT_PERIOD = 15
    
    def __init__(self, total_salary):
        self.total_salary = total_salary
        
    def calculate_salary_dialy(self):
        return self.total_salary / self.PAYMENT_PERIOD
    