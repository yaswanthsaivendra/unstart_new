from django.db import models
from django.contrib.auth.models import User
from teacher.models import Course

# Create your models here.


class Payment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_payemnts')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_payments')
    merchant_transaction_id = models.CharField(max_length=2000)
    status = models.BooleanField(default=False)


    def __str__(self) -> str:
        return f"{self.student} bought {self.course}"
