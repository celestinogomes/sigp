from django.db import models
from custom.models import *
from django.contrib.auth.models import User
from project.models import Program

class Funsionariu(models.Model):
    USER_LEVELS = [
        ('admin', 'Admin'),
        ('diretor', 'Diretor'),
        ('finance', 'Finance'),
        ('focal_point', 'Focal Point'),
    ]

    nu_registu = models.CharField(primary_key=True, unique=True, max_length=20, verbose_name='Numeru Registu')
    naran_kompletu = models.CharField(max_length=50, verbose_name='Naran Kompletu')
    lug_nasc = models.CharField(max_length=20, verbose_name='Fatin Moris')
    data_nasc = models.DateField(verbose_name='Data Moris')
    data_hahu = models.DateField(verbose_name='Data Hahu')
    hftin_atual = models.CharField(max_length=25, verbose_name='Hela Fatin Atual')
    nu_kontakt = models.CharField(max_length=15, verbose_name='Numeru Kontaktu')
    email = models.EmailField(verbose_name='Email')
    program = models.ManyToManyField(Program, verbose_name='Programa', null=True, blank=True)
    department = models.ForeignKey(Departamento, on_delete=models.CASCADE, verbose_name='Departamento')
    pozisaun = models.ForeignKey(Pozisaun, on_delete=models.CASCADE, verbose_name='Pozisaun')
    user_level = models.CharField(max_length=20, choices=USER_LEVELS, default='staff', verbose_name='User Level')
    is_active = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name="employeeuser")

    def __str__(self):
        return self.naran_kompletu