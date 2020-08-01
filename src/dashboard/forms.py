from django import forms
from models import Global

class DateRangeSelector(forms.Form):
    from_date = forms.DateField(label="From Date",widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    to_date = forms.DateField(label="To Date",widget=forms.widgets.DateInput(attrs={'type': 'date'}))

class DateSelector(forms.Form):
    date = forms.DateField(label="Date",widget=forms.widgets.DateInput(attrs={'type': 'date'}))

class StudentsReportSelector(forms.Form):
    division = forms.ChoiceField(choices=Global.division_choices)
    from_date = forms.DateField(label="From Date",widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    to_date = forms.DateField(label="To Date",widget=forms.widgets.DateInput(attrs={'type': 'date'}))
