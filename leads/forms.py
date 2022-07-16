from unicodedata import category
from django import forms
from .models import Agent, Category, Lead
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth import get_user_model

User = get_user_model()

class LeadModelForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            "ismi",
            "familiasi",
            "yoshi",
            "agent",
        )

class LeadForm(forms.Form):
    name = forms.CharField(max_length=25)
    sorname = forms.CharField(max_length=25)
    age = forms.IntegerField(min_value=0)


class NewUserForm(UserCreationForm):
        class Meta:
            model = User
            fields = ("username",)
            field_classes = {'username': UsernameField}


class AssignAgentForm(forms.Form):
    agent = forms.ModelChoiceField(queryset = Agent.objects.none())

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        agents = Agent.objects.filter(profil = request.user.userprofil)
        super(AssignAgentForm, self).__init__(*args, **kwargs)
        self.fields['agent'].queryset = agents


class LeadCategoryUpdateFrom(forms.ModelForm):
    class Meta:
        model = Lead
        fields = [
            'kategoriya',
        ]
    
