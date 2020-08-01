from django import forms
import datetime
from models import Global


class LectureSelectorForm(forms.Form):
    std = forms.ChoiceField(choices=Global.std_choices,label="Class")
    subject = forms.ChoiceField(choices=Global.subject_choices)
    division = forms.ChoiceField(choices=Global.division_choices)
    lecturer = forms.ChoiceField(choices = Global.lecturer_choices)
    file = forms.FileField()

class ExpectedStudentsInsertForm(forms.Form):
    std = forms.ChoiceField(choices=Global.std_choices,label="Class")
    subject = forms.ChoiceField(choices=Global.subject_choices)
    division = forms.ChoiceField(choices=Global.division_choices)
    lecturer = forms.ChoiceField(choices = Global.lecturer_choices)
    start_roll_num = forms.IntegerField(label="Start Roll Number")
    end_roll_num = forms.IntegerField(label = "End Roll Number")
    skip_roll_nums = forms.CharField(required=False,empty_value=None,label = "Skip Roll Numbers",widget=forms.TextInput(attrs={'placeholder': 'Separated By Space'}))
