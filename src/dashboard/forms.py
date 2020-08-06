from django import forms
from models import Global

from upload.models import Division
from django.contrib.auth.forms import AuthenticationForm

class MyModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name

class TeachersReportSelector(forms.Form):
    std = forms.ChoiceField(choices=Global.std_choices,label="Class")
    from_date = forms.DateField(label="From Date",widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    to_date = forms.DateField(label="To Date",widget=forms.widgets.DateInput(attrs={'type': 'date'}))

class ExploreLecturesForm(forms.Form):
    std = forms.ChoiceField(choices=Global.std_choices,label="Class")
    date = forms.DateField(label="Date",widget=forms.widgets.DateInput(attrs={'type': 'date'}))

class StudentsReportSelector(forms.Form):
    std = forms.ChoiceField(choices=Global.std_choices,label="Class")
    division = MyModelChoiceField(queryset=Division.objects.order_by("name"),to_field_name="name",initial=0)
    from_date = forms.DateField(label="From Date",widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    to_date = forms.DateField(label="To Date",widget=forms.widgets.DateInput(attrs={'type': 'date'}))


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'id_username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={"class":"form-control",'autocomplete': 'off','data-toggle': 'password',"id":"id_password"}
))
