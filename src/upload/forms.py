from django import forms
import datetime
from models import Global
from .models import Division, Subject

from django.contrib.auth.models import User
from django.db.models import F

class MyModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class LectureSelectorForm(forms.Form):
    std = forms.ChoiceField(choices=Global.std_choices,label="Class")
    subject = MyModelChoiceField(queryset=Subject.objects.order_by("name"),to_field_name="code",initial=0)
    division = MyModelChoiceField(queryset=Division.objects.order_by("name"),to_field_name="name",initial=0)
    file = forms.FileField()

class ExpectedStudentsInsertForm(forms.Form):
    std = forms.ChoiceField(choices=Global.std_choices,label="Class")
    subject = MyModelChoiceField(queryset=Subject.objects.order_by("name"),to_field_name="code",initial=0)
    division = MyModelChoiceField(queryset=Division.objects.order_by("name"),to_field_name="name",initial=0)
    lecturer = MyModelChoiceField(queryset=User.objects.exclude(profile__code="ADMIN").select_related("profile").annotate(code=F("profile__code"),name=F("profile__fullname")) ,to_field_name="code",initial=0)
    start_roll_num = forms.IntegerField(label="Start Roll Number")
    end_roll_num = forms.IntegerField(label = "End Roll Number")
    skip_roll_nums = forms.CharField(required=False,empty_value=None,label = "Skip Roll Numbers",widget=forms.TextInput(attrs={'placeholder': 'Separated By Space'}))

class DivisionSelectorForm(forms.Form):
    division = MyModelChoiceField(queryset=Division.objects.order_by("name"),to_field_name="name",initial=0)
