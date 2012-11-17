from django import forms
from django.forms import ModelForm
from handbook.models import Content, Node

class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'cols': 120, 'rows': 30}),
        }

class NodeForm(forms.ModelForm):
    class Meta:
        model = Node
        fields = ('title', 'slug')
