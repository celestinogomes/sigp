
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, HTML
from django.db.models import Q
from .models import Project, ProjectLocation, ProjectJustification, ProjectStatus
from custom.models import AdministrativePost, Village, Aldeia


class DateInput(forms.DateInput):
	input_type = 'date'



class ProjectForm(forms.ModelForm):

	class Meta:
		model = Project
		fields = ['name','program','sub_program','owner','fund','type', 'year', 'owner_estimation']

	def __init__(self, *args, **kwargs):
		super(ProjectForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			if isinstance(field.widget, forms.Select):
				field.widget.attrs.update({'class': 'form-select'})
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.form_tag = False
		self.fields['program'].required =True
		self.fields['sub_program'].required =True
		self.fields['owner'].required =True
		self.fields['fund'].required =True
		self.fields['type'].required =True
		
		self.helper.layout = Layout(
			Row(
				Column('name', css_class='col-md-12 mb-3'),
				css_class='row' 
			),
			Row(
				Column('program', css_class='col-md-4 mb-3'),
				Column('sub_program', css_class='col-md-4 mb-3'),
				Column('owner', css_class='col-md-4 mb-3'),
				css_class='row' 
			),
			Row(
				Column('fund', css_class='col-md-4 mb-3'),
				Column('type', css_class='col-md-4 mb-3'),
				Column('year', css_class='col-md-4 mb-3'),
				css_class='row' 
			),
			Row(
				Column('owner_estimation', css_class='col-md-12 mb-3'),
				css_class='row'
			),
		)
		

class ProjectLocationForm(forms.ModelForm):
	class Meta:
		model = ProjectLocation
		fields = ['municipality', 'administrative_post', 'village', 'aldeia', 'latitude_start', 'longitude_start', 'latitude_end', 'longitude_end']


	def __init__(self, *args, **kwargs):
		super(ProjectLocationForm, self).__init__(*args, **kwargs)
		
		for field_name, field in self.fields.items():
			if isinstance(field.widget, forms.Select):
				field.widget.attrs.update({'class': 'form-select'})
		
		self.fields['administrative_post'].queryset = AdministrativePost.objects.none()
		self.fields['village'].queryset = Village.objects.none()
		self.fields['aldeia'].queryset = Village.objects.none()

		if 'municipality' in self.data:
			try:
				municipality_id = int(self.data.get('municipality'))
				self.fields['administrative_post'].queryset = AdministrativePost.objects.filter(municipality_id=municipality_id).order_by('name')
			except (ValueError, TypeError):
				pass
		elif self.instance.pk and self.instance.municipality:
			self.fields['administrative_post'].queryset = self.instance.municipality.administrative_post.all().order_by('name')

		if 'administrative_post' in self.data:
			try:
				post_id = int(self.data.get('administrative_post'))
				self.fields['village'].queryset = Village.objects.filter(administrative_post_id=post_id).order_by('name')
			except (ValueError, TypeError):
				pass
		elif self.instance.pk and self.instance.administrative_post:
			self.fields['village'].queryset = self.instance.administrative_post.village.all().order_by('name')
			

		if 'village' in self.data:
			try:
				village_id = int(self.data.get('village'))
				self.fields['aldeia'].queryset = Aldeia.objects.filter(village_id=village_id).order_by('name')
			except (ValueError, TypeError):
				pass
		elif self.instance.pk and self.instance.village:
			self.fields['aldeia'].queryset = self.instance.village.aldeia.all().order_by('name')

		self.helper = FormHelper()
		self.helper.form_tag = False
		self.helper.layout = Layout(
			Row(
				Column('municipality', css_class='col-md-3 mb-3'),
				Column('administrative_post', css_class='col-md-3 mb-3'),
				Column('village', css_class='col-md-3 mb-3'),
				Column('aldeia', css_class='col-md-3 mb-3'),
				css_class='row'
			),
		
			#Aumenta latitude no longitude
	
		    Row(
				Column('latitude_start', css_class='col-md-3 mb-3'),
				Column('longitude_start', css_class='col-md-3 mb-3'),
				Column('latitude_end', css_class='col-md-3 mb-3'),
				Column('longitude_end', css_class='col-md-3 mb-3'),
				css_class='row'
			),	
		)					



class ProjectStatusForm(forms.ModelForm):
	date = forms.DateField(label='Data Hadia Estadu', widget=DateInput(attrs={'class':'form-control input-default',}))
	class Meta:
		model = ProjectStatus
		fields = ['status','date','description']

	def __init__(self, *args, **kwargs):
		super(ProjectStatusForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			if isinstance(field.widget, forms.Select):
				field.widget.attrs.update({'class': 'form-select'})
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.form_tag = False
		self.fields['status'].required =True
		self.fields['date'].required =True
		self.helper.layout = Layout(
			Row(
				Column('status', css_class='col-md-6 mb-3'),
				Column('date', css_class='col-md-6 mb-3'),
				css_class='row' 
			),
			Row(
				Column('description', css_class='col-md-12 mb-3'),
				css_class='row' 
			),
		)



class ProjectJustificationForm(forms.ModelForm):
	date = forms.DateField(label='Data Hadia Justifikasaun', widget=DateInput(attrs={'class':'form-control input-default',}))
	class Meta:
		model = ProjectJustification
		fields = ['date','description']

	def __init__(self, *args, **kwargs):
		super(ProjectJustificationForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			if isinstance(field.widget, forms.Select):
				field.widget.attrs.update({'class': 'form-select'})
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.form_tag = False
		self.fields['date'].required =True
		self.helper.layout = Layout(
			Row(
				Column('date', css_class='col-md-12 mb-3'),
				css_class='row' 
			),
			Row(
				Column('description', css_class='col-md-12 mb-3'),
				css_class='row' 
			),
		)