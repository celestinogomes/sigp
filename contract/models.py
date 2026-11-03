from django.db import models
import uuid
from decimal import Decimal
from project.models import Project, Company, Status
from django.contrib.auth.models import User

class Contract(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Projeto", related_name="contract_project")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Kompanha/Vendors", related_name="contract_company")
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Status", related_name="contract_status")
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    number = models.CharField(max_length=100, null=True,blank=True)
    amount = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    is_active = models.BooleanField(default=False, null=True, blank=True)
    datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,  blank=True, related_name="contract_user")
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=True, blank=True)

    class Meta:
        verbose_name = "Kontratu Projeto Original"
        verbose_name_plural = "Lista Kontratu Projeto"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Contract value may have changed, so recalculate the bank guarantee amounts.
        for bank_guarantee in self.contract_bank_guarantee.all():
            bank_guarantee.save()

    def __str__(self):
        return f'{self.project.name} - {self.company}'
    

class ContractAmendment(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name="project_contract_amendment")
    amendment_contract_number = models.CharField(max_length=100, null=True, blank=True)
    amendment_end_date = models.DateField(null=True, blank=True)
    amendment_amount = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="contract_amendment_user")
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Contract value changed, so recalculate the bank guarantee amounts.
        for bank_guarantee in BankGuarantee.objects.filter(contract__project=self.project):
            bank_guarantee.save()

    def __str__(self):
        return f" {self.project.name} - {self.amendment_amount}"

class BankGuarantee(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name="contract_bank_guarantee")
    performance_security = models.PositiveIntegerField(null=True, blank=True)
    performance_security_amount = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
    advance_payment = models.PositiveIntegerField(null=True, blank=True)
    amount_advance_payment = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
    retention = models.PositiveIntegerField(null=True, blank=True)
    retention_amount = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="bank_guarantee_user")
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=True, blank=True)

    def __str__(self):
        return f" {self.contract.project.name} - {self.performance_security_amount}"