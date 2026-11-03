from django.db import models
from django.contrib.auth.models import User
from project.models import Project
import uuid

class Payment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, related_name="payment_project")
    description = models.CharField(max_length=200, null=True)
    contract_amount = models.DecimalField(max_digits=11, decimal_places=2, default=0.00)
    physical_progress = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    payment_amount = models.DecimalField(max_digits=11, decimal_places=2, default=0.00)
    comulative_amount = models.DecimalField(max_digits=11, decimal_places=2, default=0.00)
    comulative_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    balance_amount = models.DecimalField(max_digits=11, decimal_places=2, default=0.00)
    balance_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    process_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    date = models.DateField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    datetime = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=True, blank=True)
    

    def __str__(self):
        template = '{0.project} {0.payment_amount} - {0.description}'
        return template.format(self)


class PaymentHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, related_name="payment_project_history")
    physical_progress = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    description = models.CharField(max_length=200, null=True, blank=True)
    contract_amount = models.DecimalField(max_digits=11, decimal_places=2, default=0.00)
    
    payment_amount = models.DecimalField(max_digits=11, decimal_places=2, default=0.00)
    comulative_amount = models.DecimalField(max_digits=11, decimal_places=2, default=0.00)
    comulative_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    balance_amount = models.DecimalField(max_digits=11, decimal_places=2, default=0.00)
    balance_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    process_number = models.CharField(max_length=100, null=True, blank=True) 
    date = models.DateField(null=True)
    datetime = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    info = models.CharField(max_length=50, null=True) 
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=True, blank=True)
    
    class Meta:
        ordering = ['date', 'datetime']

    def __str__(self):
        template = '{0.project} {0.info} ({0.date})'
        return template.format(self)