from django import forms
from project.models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, HTML



class ProgramForm(forms.ModelForm):
	class Meta:
		model = Program
		fields = ['name', 'code']

	def __init__(self, *args, **kwargs):
		super(ProgramForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.fields['name'].required = True
		self.helper.layout = Layout(
			Row(
				Column('code', css_class='form-group col-md-12 mb-0'),
			),
			Row(
				Column('name', css_class='form-group col-md-12 mb-0'),
			),
			HTML("""
                <div class="mt-3">
                    <button class="btn btn-primary" type="submit" title="Save">
                        Save <i class='fa fa-save'></i>
                    </button>
                </div>
            """)
		)


class SubProgramForm(forms.ModelForm):
	class Meta:
		model = SubProgram
		fields = ['program', 'name', 'code']

	def __init__(self, *args, **kwargs):
		super(SubProgramForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			if isinstance(field.widget, forms.Select):
				field.widget.attrs.update({'class': 'form-select'})
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.fields['name'].required = True
		self.helper.layout = Layout(
			Row(
				Column('program', css_class='form-group col-md-12 mb-0'),
			),
			Row(
				Column('code', css_class='form-group col-md-12 mb-0'),
			),
			Row(
				Column('name', css_class='form-group col-md-12 mb-0'),
			),
			HTML("""
                <div class="mt-3">
                    <button class="btn btn-primary" type="submit" title="Save">
                        Save <i class='fa fa-save'></i>
                    </button>
                </div>
            """)
		)


class OwnerForm(forms.ModelForm):
	class Meta:
		model = Owner
		fields = ['name', 'code']

	def __init__(self, *args, **kwargs):
		super(OwnerForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.fields['name'].required = True
		self.helper.layout = Layout(
			Row(
				Column('code', css_class='form-group col-md-12 mb-0'),
			),
			Row(
				Column('name', css_class='form-group col-md-12 mb-0'),
			),
			HTML("""
                <div class="mt-3">
                    <button class="btn btn-primary" type="submit" title="Save">
                        Save <i class='fa fa-save'></i>
                    </button>
                </div>
            """)
		)


class FundForm(forms.ModelForm):
	class Meta:
		model = Fund
		fields = ['name', 'code']

	def __init__(self, *args, **kwargs):
		super(FundForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.fields['name'].required = True
		self.helper.layout = Layout(
			Row(
				Column('code', css_class='form-group col-md-12 mb-0'),
			),
			Row(
				Column('name', css_class='form-group col-md-12 mb-0'),
			),
			HTML("""
                <div class="mt-3">
                    <button class="btn btn-primary" type="submit" title="Save">
                        Save <i class='fa fa-save'></i>
                    </button>
                </div>
            """)
		)
		
class TypeForm(forms.ModelForm):
	class Meta:
		model = Type
		fields = ['name']

	def __init__(self, *args, **kwargs):
		super(TypeForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.fields['name'].required = True
		self.helper.layout = Layout(
			
			Row(
				Column('name', css_class='form-group col-md-12 mb-0'),
			),
			HTML("""
                <div class="mt-3">
                    <button class="btn btn-primary" type="submit" title="Save">
                        Save <i class='fa fa-save'></i>
                    </button>
                </div>
            """)
		)