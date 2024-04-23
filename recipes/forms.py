from django import forms
from django.forms import (
    Form,
    ModelForm,
    MultiWidget,
    MultiValueField,
    TextInput,
    Textarea,
    SelectMultiple,
    formset_factory
)
from .models import Recipe, Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        labels = {
            'content': 'Your comment:'
        }

class RatingForm(forms.Form):
    RATING_STARS = [(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    rating = forms.ChoiceField(choices=RATING_STARS, widget=forms.RadioSelect)

class RecipeForm(ModelForm):
    '''
    Form class to create a recipe form without excluding ingredients or preparation.
    '''
    class Meta:
        model = Recipe
        fields = [
            'title',
            'recipe_image',
            'ingredients',
            'preparation',
            'category',
            'cooking_duration',
            'servings',
            'make_public'
        ]
        labels = {
            'make_public': 'Make Public',
            'cooking_duration': 'Cooking duration (minutes)'
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter recipe title'
            }),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
