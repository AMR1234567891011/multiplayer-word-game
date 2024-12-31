from django import forms
from .models import wordG

class wordform(forms.ModelForm):
    class Meta:
        model = wordG
        fields = ['argument']
    argument = forms.CharField(label='', max_length = 5)
