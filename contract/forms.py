from django import forms
from contract.models import Contract
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, HTML



class DateInput(forms.DateInput):
	input_type = 'date'
	


class ContractForm(forms.ModelForm):
	start_date = forms.DateField(label='Data Inicio Kontratu', widget=DateInput(attrs={'class':'form-control input-default',}))
	end_date = forms.DateField(label='Data Remata Kontratu', widget=DateInput(attrs={'class':'form-control input-default'}))
	class Meta:
		model = Contract
		fields = ['company', 'status', 'start_date', 'end_date', 'number', 'amount']

	def __init__(self, *args, **kwargs):
		super(ContractForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			if isinstance(field.widget, forms.Select):
				field.widget.attrs.update({'class': 'form-select'})
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.form_tag = False
		self.fields['start_date'].required = False
		self.fields['end_date'].required = False
		self.fields['status'].required = True
		self.helper.layout = Layout(
			
			Row(
				Column('number', css_class='form-group col-md-4 mb-3'),
				Column('amount', css_class='form-group col-md-4 mb-3'),
				Column('company', css_class='form-group col-md-4 mb-3'),
				css_class='row'
			),
			Row(
				Column('start_date', css_class='form-group col-md-4 mb-0'),
				Column('end_date', css_class='form-group col-md-4 mb-0'),
				Column('status', css_class='form-group col-md-4 mb-0'),
				css_class='row'
			),
		)