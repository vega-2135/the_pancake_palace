from django import forms
from django.forms import (
    ModelForm,
)

from .models import Comment, Recipe


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
    Form class to create a recipe form without excluding ingredients
    or preparation.
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
            'cooking_duration': 'Cooking duration (minutes)',
            'ingredients': 'Ingredients (add as in the example below)',
            'preparation': 'Preparation (add as in the example below)'
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter recipe title'
            }),
            'ingredients': forms.Textarea(attrs={
                'placeholder': '1 cup flour, 1 cup milk...',
                'rows': 8,
                'cols': 10
            }),
            'preparation': forms.Textarea(attrs={
                'placeholder': "Step 1: Add ingredients..,"
                "Step 2: Cook mixture..,,",
                'rows': 8,
                'cols': 10
            })
        }
