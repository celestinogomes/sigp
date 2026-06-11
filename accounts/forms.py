from django import forms
from django.contrib.auth.models import User, Group
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML, Div


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML(""" <div class="row"> """),
            Column('username', css_class="col"),
            Column('email', css_class="col"),
            HTML(""" </div> """),
            HTML(""" <div class="row"> """),
            Column('first_name', css_class="col"),
            Column('last_name', css_class="col"),
            HTML(""" </div> """),
            Div(
                Submit('submit', 'Update Profile', css_class='btn btn-primary text-center col-md-12 mt-2'),
                css_class='text-center'
            )
        )