from django import forms
from payment.models import Payment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, HTML



class DateInput(forms.DateInput):
	input_type = 'date'
	

class PaymentForm(forms.ModelForm):
	date = forms.DateField(label='Data Pagamanto', widget=DateInput(attrs={'class':'form-control input-default',}))
	class Meta:
		model = Payment
		fields = ['payment_amount', 'date', 'description', 'process_number', 'physical_progress']

	def __init__(self, *args, **kwargs):
		super(PaymentForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			if isinstance(field.widget, forms.Select):
				field.widget.attrs.update({'class': 'form-select'})
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.form_tag = False
		self.fields['payment_amount'].required = True
		self.fields['date'].required = True
		self.fields['description'].required = True
		self.fields['process_number'].required = False
		self.fields['physical_progress'].label = 'Progresu Fisiku'
		self.helper.layout = Layout(
			
			Row(
				Column('date', css_class='form-group col-md-6 mb-3'),
				Column('physical_progress', css_class='form-group col-md-6 mb-3'),
				css_class='row'
			),
			Row(
				Column('payment_amount', css_class='form-group col-md-6 mb-3'),
				Column('process_number', css_class='form-group col-md-6 mb-3'),
				css_class='row'
			),
			Row(
				Column('description', css_class='form-group col-md-12 mb-3'),
				css_class='row'
			),
		)