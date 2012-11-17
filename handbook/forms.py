from django import forms
from django.forms import ModelForm
from handbook.models import Content

class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'cols': 120, 'rows': 30}),
        }
