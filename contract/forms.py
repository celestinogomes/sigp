from django import forms
from contract.models import Contract, BankGuarantee
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


class BankGuaranteeForm(forms.ModelForm):
	performance_security = forms.DecimalField(label='Performance Security (%)', required=False, min_value=0, max_value=100, decimal_places=2)
	performance_security_amount = forms.DecimalField(label='Performance Security Amount', required=False, decimal_places=2, max_digits=11)
	advance_payment = forms.DecimalField(label='Advance Payment (%)', required=False, min_value=0, max_value=100, decimal_places=2)
	amount_advance_payment = forms.DecimalField(label='Advance Payment Amount', required=False, decimal_places=2, max_digits=11)
	retention = forms.DecimalField(label='Retention (%)', required=False, min_value=0, max_value=100, decimal_places=2)
	retention_amount = forms.DecimalField(label='Retention Amount', required=False, decimal_places=2, max_digits=11)

	percent_fields = ['performance_security', 'advance_payment', 'retention']

	class Meta:
		model = BankGuarantee
		fields = ['performance_security', 'advance_payment', 'retention', 'performance_security_amount', 'amount_advance_payment', 'retention_amount']

	def __init__(self, *args, **kwargs):
		super(BankGuaranteeForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.form_tag = False
		self.helper.layout = Layout(
			Row(
				Column('performance_security', css_class='form-group col-md-2 mb-3'),
				Column('performance_security_amount', css_class='form-group col-md-2 mb-3'),
				Column('advance_payment', css_class='form-group col-md-2 mb-3'),
				Column('amount_advance_payment', css_class='form-group col-md-2 mb-3'),
				Column('retention', css_class='form-group col-md-2 mb-3'),
				Column('retention_amount', css_class='form-group col-md-2 mb-3'),
				css_class='row'
			),
		)
