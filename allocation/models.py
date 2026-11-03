from django.db import models
from project.models import Project
from custom.models import Ano
from django.contrib.auth.models import User
import uuid

class Allocation(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True, related_name="project_allocation")
    activity_code = models.CharField(max_length=50, null=True, blank=True, verbose_name="Kodigo Atividade")
    year = models.ForeignKey(Ano, on_delete=models.CASCADE, null=True, blank=True, related_name="project_allocation_year")
    allocation_original = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True, verbose_name="Montante Alokasaun")
    allocation_total = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True, verbose_name="Montante Alokasaun Total")
    execution_amount = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True, verbose_name="Montante Ezekusaun")
    execution_percent = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Taxa Ezekusaun (%)")
    contract_balance = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True, verbose_name="Balansu Alokasaun")
    balance_percent = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Balansu Ezekusaun (%)")
    datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_lock = models.BooleanField(default=False, null=True, blank=True)
    is_active = models.BooleanField(default=False, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=True, blank=True)
    def __str__(self):
        return f"{self.project}-{self.year}-{self.allocation_original}"
    

class Transferencia(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True, related_name="transferencia_project")
    allocation = models.ForeignKey(Allocation, on_delete=models.CASCADE, null=True, blank=True, related_name="transferencia_allocation")
    date = models.DateField(null=True, blank=True)
    transferencia = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True, verbose_name="Montante Transferencia")
    allocation_total = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True, verbose_name="Montante Alokasaun Total")
    comments = models.TextField(null=True, blank=True)
    is_lock = models.BooleanField(default=False, null=True, blank=True)
    is_active = models.BooleanField(default=False, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.project}-{self.transferencia}"
    


