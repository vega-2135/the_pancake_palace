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

class IngredientsWidget(MultiWidget, TextInput):
    '''
    A widget that is composed of multiple widgets.
    '''
    def __init__(self):
        widgets = [
            forms.TextInput(attrs={
                'placeholder': 'Enter Ingredient',
                'required': True
            }),
            forms.TextInput(attrs={
                'placeholder': 'Enter Amount',
                'required': True
            })
        ]
        super().__init__(widgets)

    # define how to extract values from data to be displayed in the widget.
    def decompress(self, value):
        if value:
            return [value['ingredient'], value['amount']]
        return ['', '']


class IngredientsField(MultiValueField):
    '''
    Define the ingredients field properties that uses the above multiwidget.
    '''
    widget = IngredientsWidget()

    def __init__(self, **kwargs):
        fields = [
            forms.CharField(max_length=50),
            forms.CharField(max_length=50),
        ]
        super().__init__(fields=fields, **kwargs)

    # define how to process the values provided into a single piece of data.
    def compress(self, data_list):
        ingredients_dict = dict(
            ingredient=data_list[1],
            amount=data_list[0]
        )
        return ingredients_dict

class IngredientsForm(Form):
    '''
    Form class for ingredients form.
    '''
    ingredients = IngredientsField(
        label='',
        help_text='Enter an ingredient and amount or remove empty fields.'
    )


class PreparationForm(Form):
    '''
    Form class for preparation steps form.
    '''
    preparation = forms.CharField(
        label='',
        help_text='Enter preparation step or remove empty fields.',
        widget=Textarea(attrs={
            'placeholder': 'Enter preparation step',
            'rows': '3',
            'required': True
        })
    )


# Create formset class to add multiple of the same form
IngredientsFormset = formset_factory(IngredientsForm)

PreparationFormset = formset_factory(PreparationForm)

