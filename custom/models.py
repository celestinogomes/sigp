from django.db import models



class Municipality(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class AdministrativePost(models.Model):
	municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, null=True, related_name='administrative_post')
	name = models.CharField(max_length=100)

	def __str__(self):
		template = '{0.name} {0.municipality}'
		return template.format(self)

class Village(models.Model):
	administrative_post = models.ForeignKey(AdministrativePost, on_delete=models.CASCADE, null=True, related_name='village')
	name = models.CharField(max_length=100)

	def __str__(self):
		template = '{0.name} {0.administrative_post}'
		return template.format(self)


class Aldeia(models.Model):
	village = models.ForeignKey(Village, on_delete=models.CASCADE, null=True, related_name='aldeia')
	name = models.CharField(max_length=100)

	def __str__(self):
		template = '{0.name} {0.village}'
		return template.format(self)
      

class Ano(models.Model):
    ano = models.IntegerField()

    def __str__(self):
        return str(self.ano)


class Departamento(models.Model):
    sigla = models.CharField(max_length=15, verbose_name='Sigla Departamento')
    departamento = models.CharField(max_length=100, verbose_name='Departamento')

    def __str__(self):
        return self.sigla

class Pozisaun(models.Model):
    pozisaun = models.CharField(max_length=30, verbose_name='Pozisaun')

    def __str__(self):
        return self.pozisaun
