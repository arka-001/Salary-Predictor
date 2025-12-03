from django.db import models

class SalaryData(models.Model):
    years = models.FloatField()
    job_level = models.IntegerField() 
    salary = models.FloatField()

    def __str__(self):
        return f"{self.years} Yrs | Lvl {self.job_level} | ₹{self.salary}"