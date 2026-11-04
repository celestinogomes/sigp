import uuid
from django.db import models
from django.contrib.auth.models import User
from custom.models import Municipality, AdministrativePost, Village, Aldeia, Ano

class Program(models.Model):
    code = models.CharField(max_length=10, null=True, blank=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.code} - {self.name}'

class SubProgram(models.Model):
    program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True, blank=True)
    code = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return f'{self.code} - {self.name}'


class Owner(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Company(models.Model):
    name = models.CharField(max_length=500, null=True)

    def __str__(self):
        return self.name
    

class Type(models.Model):
    name = models.CharField(max_length=500, null=True)

    def __str__(self):
        return self.name
    

class Status(models.Model):
    name = models.CharField(max_length=500, null=True)

    def __str__(self):
        return self.name

class Fund(models.Model):
    code = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=100)
    desc = models.TextField(blank=True)

    def __str__(self):
        return f'{self.code} - {self.name}'


class Project(models.Model):
    name = models.CharField(max_length=500, verbose_name="Projeto")
    activity_code = models.CharField(max_length=50, null=True, blank=True, verbose_name="Kodigo Atividade")
    program = models.ForeignKey(Program, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Programa", related_name="project_program")
    sub_program = models.ForeignKey(SubProgram, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Sub Programa", related_name="project_sub_program")
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, null=True, blank=True, related_name="project_owner")
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Fontes Orsamento", related_name="project_fund")
    type = models.ForeignKey(Type, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Tipo Projeto", related_name='project_type')
    year = models.ForeignKey(Ano, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Tinan Plano Projeto", related_name='project_year')
    owner_estimation = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    is_active = models.BooleanField(default=False, null=True, blank=True)
    datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,  blank=True, related_name="project_user")
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=True, blank=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Projeto"
        verbose_name_plural = "Lista Projeto"


class ProjectLocation(models.Model):
    project = models.OneToOneField( Project, on_delete=models.CASCADE, null=True, blank=True, related_name="project_location")
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, null=True, blank=True, related_name="project_location_municipality", verbose_name="Municipio" )
    administrative_post = models.ForeignKey(AdministrativePost, on_delete=models.CASCADE, null=True, blank=True, related_name="project_location_administrativepost", verbose_name="Posto Administrativo" )
    village = models.ForeignKey(Village, on_delete=models.CASCADE, null=True, blank=True, related_name="project_location_village", verbose_name="Suco")
    aldeia = models.ForeignKey(Aldeia, on_delete=models.CASCADE, null=True, blank=True, related_name="project_location_aldeia", verbose_name="Aldeia")
    latitude_start = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True, verbose_name="Latitude Inisiu")
    longitude_start = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True, verbose_name="Longitude Inisiu")
    latitude_end = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True, verbose_name="Latitude Remata")
    longitude_end = models.DecimalField(max_digits=20,decimal_places=6, null=True, blank=True, verbose_name="Longitude Remata")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,  blank=True, related_name="project_location_user")
    # uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=True, blank=True)
    
    
    def __str__(self):
        try:
            return f"{self.project.name} - {self.municipality.name}"
        except:
            return f"Location {self.id}"

    class Meta:
        verbose_name = "Lokalizasaun Projeto"
        verbose_name_plural = "Lista Lokalizasaun Projeto"


class ProjectStatus(models.Model):
    project = models.ForeignKey( Project, on_delete=models.CASCADE, null=True, blank=True, related_name="project_status")
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Status", related_name="project_status")
    date = models.DateField(null=True, blank=True, verbose_name="Data Update Status")
    description = models.CharField(max_length=200, null=True, blank=True, verbose_name="Komentariu")
    datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,  blank=True, related_name="project_status_user")
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=True, blank=True)
    def __str__(self):
        return f"{self.project} - {self.status}"
    class Meta:
        verbose_name = "Status Projeto"


class ProjectJustification(models.Model):
    project = models.ForeignKey( Project, on_delete=models.CASCADE, null=True, blank=True, related_name="project_justification")
    date = models.DateField(null=True, blank=True, verbose_name="Data Update Fo Justifikasaun")
    description = models.TextField(blank=True, verbose_name="Komentariu")
    datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,  blank=True, related_name="justification_user")
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=True, blank=True)
    def __str__(self):
        return f"{self.project} - {self.date}"
    class Meta:
        verbose_name = "Justifikasaun Projeto"


