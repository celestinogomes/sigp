from django.db import models

class Program(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class SubProgram(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class Owner(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Company(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Fund(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=250)
    activity_code = models.CharField(max_length=50, null=True, blank=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
