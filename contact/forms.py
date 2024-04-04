from .models import ReachOut
from django import forms


class ReachOutForm(forms.ModelForm):
    class Meta:
        model = ReachOut
        fields = ('name', 'email', 'message')