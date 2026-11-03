from django.test import TestCase
from project.models import *


class AmendmentPeriod(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, related_name='project_amendmentperiod')
    number = models.CharField(max_length=100, null=True)
    end_date = models.DateField(null=True)
    comment = models.CharField(max_length=20, null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=True, blank=True)
    
    def __str__(self):
        return f" {self.project.name} - {self.end_date}"

class AmendmentAmount(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, related_name='project_amendmentamount')
    number = models.CharField(max_length=100, null=True, blank=True)
    amendment_amount = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
    total_amendment_amount = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
    comment = models.CharField(max_length=20, null=True, blank=True)
    datetime = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=True, blank=True)
    
    def __str__(self):
        return f" {self.project.name} - {self.total_amendment_amount}"

