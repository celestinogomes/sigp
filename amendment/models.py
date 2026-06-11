from django.db import models
from django.contrib.auth.models import User
from project.models import Project
import uuid


class AmendmenAmount(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True, related_name="amendment_amount_project")
    number = models.CharField(max_length=200, null=True, blank=True, verbose_name="Nu. Kontratu")
    date = models.DateField(null=True, blank=True)
    amount = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True, verbose_name="Montante")
    amount_total = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True, verbose_name="Montante Total")
    comments = models.TextField(null=True, blank=True)
    datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=True, blank=True)
    def __str__(self):
        return f"{self.project}-{self.amount}-{self.amount_total}"


class AmendmenTime(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True, related_name="amendment_time_project")
    number = models.CharField(max_length=200, null=True, blank=True, verbose_name="Nu. Kontratu")
    date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True, verbose_name="Data Remata Foun")
    comments = models.TextField(null=True, blank=True)
    datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=True, blank=True)
    def __str__(self):
        return f"{self.project}-{self.date}"
