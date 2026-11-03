from django import forms
from allocation.models import Allocation, Transferencia
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, HTML



class DateInput(forms.DateInput):
	input_type = 'date'
	


class AllocationForm(forms.ModelForm):
	class Meta:
		model = Allocation
		fields = ['year', 'allocation_original', 'activity_code']

	def __init__(self, *args, **kwargs):
		super(AllocationForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			if isinstance(field.widget, forms.Select):
				field.widget.attrs.update({'class': 'form-select'})
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.form_tag = False
		self.fields['year'].required = True
		self.fields['activity_code'].required = False
		self.fields['allocation_original'].required = True
		self.helper.layout = Layout(
			
			Row(
				Column('year', css_class='form-group col-md-4 mb-3'),
				Column('activity_code', css_class='form-group col-md-4 mb-3'),
				Column('allocation_original', css_class='form-group col-md-4 mb-3'),
				css_class='row'
			),
		)
		

class TransferenciaForm(forms.ModelForm):
	date = forms.DateField(label='Data', widget=DateInput(attrs={'class':'form-control input-default',}))
	class Meta:
		model = Transferencia
		fields = ['date', 'transferencia', 'comments']

	def __init__(self, *args, **kwargs):
		super(TransferenciaForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			if isinstance(field.widget, forms.Select):
				field.widget.attrs.update({'class': 'form-select'})
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.form_tag = False
		self.fields['date'].required = True
		self.fields['transferencia'].required = False
		self.helper.layout = Layout(
			
			Row(
				Column('date', css_class='form-group col-md-6 mb-3'),
				Column('transferencia', css_class='form-group col-md-6 mb-3'),
				css_class='row'
			),
			Row(
				Column('comments', css_class='form-group col-md-12 mb-3'),
				css_class='row'
			),
		)