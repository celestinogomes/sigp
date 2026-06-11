from django import forms
from funsionariu.models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, HTML, Field, Div
from crispy_forms.bootstrap import TabHolder, Tab

class DateInput(forms.DateInput):
    input_type = 'date'

class FunsionariuForm(forms.ModelForm):
    data_nasc = forms.DateField(label='Data Moris', widget=DateInput(attrs={'class':'form-control input-default'}))
    data_hahu = forms.DateField(label='Data Hahu', widget=DateInput(attrs={'class':'form-control input-default'}))
    
    class Meta:
        model = Funsionariu     
        fields = '__all__'
        widgets = {
            'program': forms.CheckboxSelectMultiple(),
            'department': forms.Select(attrs={'class':'form-control input-default'}),
            'pozisaun': forms.Select(attrs={'class':'form-control input-default'}),
            'user_level': forms.Select(attrs={'class':'form-control input-default'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        
        for field_name, field in self.fields.items():
            if field_name not in ['data_nasc', 'data_hahu', 'department', 'pozisaun', 'user_level', 'program']:
                field.widget.attrs.update({'class': 'form-control input-default'})

        self.helper.layout = Layout(
            HTML(""" <div class="row mt-2"> """),
            Column('nu_registu', css_class="col-md-3 col-sm-6"),
            Column('naran_kompletu', css_class="col-md-3 col-sm-6"),
            Column('lug_nasc', css_class="col-md-3 col-sm-6"),
            Column('data_nasc', css_class="col-md-3 col-sm-6"),
            HTML(""" </div> """),
            
            HTML(""" <div class="row mt-2"> """),
            Column('data_hahu', css_class="col-md-3 col-sm-6"),
            Column('hftin_atual', css_class="col-md-3 col-sm-6"),
            Column('nu_kontakt', css_class="col-md-3 col-sm-6"),
            Column('email', css_class="col-md-3 col-sm-6"), # Email digeser ke baris kedua agar layout penuh
            HTML(""" </div> """),
            
            HTML(""" <div class="row mt-2"> """),
            Column('department', css_class="col-md-4 col-sm-12"),
            Column('pozisaun', css_class="col-md-4 col-sm-12"),
            Column('user_level', css_class="col-md-4 col-sm-12"),
            HTML(""" </div> """),

            HTML(""" <div class="row mt-3"> """),
            Column('program', css_class="col-12 program-checkbox-list"),
            HTML(""" </div> """),
            
            HTML(""" <div class="text-center mt-4"> """),
            HTML(""" <button class="btn btn-success btn-md px-4 me-2" id="toastr-success-bottom-center" type="submit">RAI</button> """),
            HTML(""" <a href="{% url 'funsionario' %}" class="btn btn-secondary btn-md px-4">CANCEL</a> """),
            HTML(""" </div> """),
        )
      



