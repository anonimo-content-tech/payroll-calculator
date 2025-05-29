import inspect

class Employee:

    def __init__(self, imss_salary, payment_period, compensation=0, double_overtime=0, christmas_bonus=0):
        frame_llamador = inspect.currentframe().f_back
        info = inspect.getframeinfo(frame_llamador)
        print(f"Instanciado desde {info.filename}, función {info.function}, línea {info.lineno}")
        print("IMSS_SALARY EN EMPLOYEE: ", imss_salary, " PAYMENT_PERIOD: ", payment_period)
        self.imss_salary = imss_salary
        self.payment_period = payment_period
        self.compensation = compensation
        self.double_overtime = double_overtime
        self.christmas_bonus = christmas_bonus

    def calculate_salary_dialy(self):
        result = self.imss_salary / self.payment_period
        print("RESULT DE DIVISIÓN: ", result)
        return 285.80

    def calculate_total_salary(self):
        return self.imss_salary + self.compensation + self.double_overtime + self.christmas_bonus
    
    def calculate_total_minimum_salary(self, smg):
        return smg + self.compensation + self.double_overtime + self.christmas_bonus
