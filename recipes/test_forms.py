from django.test import TestCase
from .forms import CommentForm
from .forms import RecipeForm
from django.core.files.uploadedfile import SimpleUploadedFile


class TestCommentForm(TestCase):

    def test_form_is_valid(self):
        comment_form = CommentForm({'content': 'This is a great post'})
        self.assertTrue(comment_form.is_valid(), msg='Form is not valid')

    def test_form_is_invalid(self):
        comment_form = CommentForm({'content': '' })
        self.assertFalse(comment_form.is_valid(), msg='Form is valid')


class TestRecipeForm(TestCase):

    def test_form_is_valid(self):
        recipe_form = RecipeForm({
            'title': 'test',
            'category': '1',
            'cooking_duration': '20',
            'servings': '2',
            'make_public': 'True',
            'recipe_image': ''
        })
        self.assertTrue(recipe_form.is_valid(), msg='Form is not valid')

    def test_title_is_required(self):
        recipe_form = RecipeForm({
            'title':''
        })
        self.assertFalse(recipe_form.is_valid(), msg='Form is not valid')

    def test_category_is_required(self):
        recipe_form = RecipeForm({
            'category':''
        })
        self.assertFalse(recipe_form.is_valid(), msg='Form is not valid')
    
    def test_cooking_time_is_required(self):
        recipe_form = RecipeForm({
            'cooking_time':''
        })
        self.assertFalse(recipe_form.is_valid(), msg='Form is not valid')

    def test_servings_is_required(self):
        recipe_form = RecipeForm({
            'servings':''
        })
        self.assertFalse(recipe_form.is_valid(), msg='Form is not valid')

    def test_make_public_is_required(self):
        recipe_form = RecipeForm({
            'make_public':''
        })
        self.assertFalse(recipe_form.is_valid(), msg='Form is not valid')




  
