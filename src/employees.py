class Employee:
    PAYMENT_PERIOD = 15
    
    def __init__(self, imss_salary, christmas_bonus=0):
        self.imss_salary = imss_salary
        self.christmas_bonus = christmas_bonus
        
    def calculate_salary_dialy(self):
        return self.imss_salary / self.PAYMENT_PERIOD
    
    def calculate_total_salary(self):
        return self.imss_salary + self.christmas_bonus