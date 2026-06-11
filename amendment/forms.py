from django import forms
from amendment.models import AmendmenAmount, AmendmenTime
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, HTML



class DateInput(forms.DateInput):
	input_type = 'date'
	


class AmendmentAmountForm(forms.ModelForm):
	date = forms.DateField(label='Data', widget=DateInput(attrs={'class':'form-control input-default',}))
	class Meta:
		model = AmendmenAmount
		fields = ['amount', 'comments', 'number','date']

	def __init__(self, *args, **kwargs):
		super(AmendmentAmountForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			if isinstance(field.widget, forms.Select):
				field.widget.attrs.update({'class': 'form-select'})
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.form_tag = False
		self.fields['amount'].required = True
		self.fields['number'].required = True
		self.helper.layout = Layout(
			
			Row(
				Column('number', css_class='form-group col-md-4 mb-3'),
				Column('amount', css_class='form-group col-md-4 mb-3'),
				Column('date', css_class='form-group col-md-4 mb-3'),
				css_class='row'
			),
			Row(
				Column('comments', css_class='form-group col-md-12 mb-3'),
				css_class='row'
			),
		)
		



class AmendmentTimeForm(forms.ModelForm):
	date = forms.DateField(label='Data', widget=DateInput(attrs={'class':'form-control input-default',}))
	end_date = forms.DateField(label='Data Remata Foun', widget=DateInput(attrs={'class':'form-control input-default',}))
	class Meta:
		model = AmendmenTime
		fields = ['date', 'comments', 'number', 'end_date']

	def __init__(self, *args, **kwargs):
		super(AmendmentTimeForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			if isinstance(field.widget, forms.Select):
				field.widget.attrs.update({'class': 'form-select'})
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.form_tag = False
		self.fields['date'].required = True
		self.fields['number'].required = True
		self.helper.layout = Layout(
			
			Row(
				Column('number', css_class='form-group col-md-4 mb-3'),
				Column('date', css_class='form-group col-md-4 mb-3'),
				Column('end_date', css_class='form-group col-md-4 mb-3'),
				css_class='row'
			),
			Row(
				Column('comments', css_class='form-group col-md-12 mb-3'),
				css_class='row'
			),
		)
		