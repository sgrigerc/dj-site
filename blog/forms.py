from cProfile import label
from ssl import HAS_TLSv1_1, HAS_TLSv1_3
from turtle import textinput
from django import forms
from django.contrib.auth.models import User
from django.http import Http404
from .models import Messages
from django.contrib.auth.forms import UserCreationForm



class UserAppealForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserAppealForm, self).__init__(*args, **kwargs)
        self.fields['subject'].label = "Тема письма"
        self.fields['email'].label = "Ваша почта"
        self.fields['text'].label = "Текст сообщения"

    class Meta:
        model = Messages
        fields = ['subject', 'email', 'text']

