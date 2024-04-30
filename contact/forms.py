from django import forms
from .models import ReachOut


class ReachOutForm(forms.ModelForm):
    class Meta:
        model = ReachOut
        fields = ('name', 'email', 'message')
