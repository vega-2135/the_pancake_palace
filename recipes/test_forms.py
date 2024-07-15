from django.test import TestCase

from .forms import CommentForm, RecipeForm


class TestCommentForm(TestCase):
    """
    Test suite for the CommentForm class.

    This class contains unit tests to ensure the CommentForm behaves correctly
    under various conditions.

    Methods:
    --------
    test_form_is_valid():
        Test that a form with valid data is recognized as valid.

    test_form_is_invalid():
        Test that a form with invalid data (e.g., empty content) is recognized
        as invalid.
    """

    def test_form_is_valid(self):
        """
        Test that a CommentForm with valid content is considered valid.

        This test verifies that when a CommentForm is provided with valid data,
        specifically a non-empty 'content' field, the form's is_valid() method
        returns True.
        """
        comment_form = CommentForm({"content": "This is a great post"})
        self.assertTrue(comment_form.is_valid(), msg="Form is not valid")

    def test_form_is_invalid(self):
        """
        Test that a CommentForm with empty content is considered invalid.

        This test checks that when a CommentForm is provided with invalid data,
        specifically an empty 'content' field, the form's is_valid() method
        returns False.
        """
        comment_form = CommentForm({"content": ""})
        self.assertFalse(comment_form.is_valid(), msg="Form is valid")


class TestRecipeForm(TestCase):
    """
    Test suite for the RecipeForm class.

    This class contains unit tests to ensure the RecipeForm behaves correctly
    under various conditions.

    Methods:
    --------
    test_form_is_valid():
        Test that a form with all valid fields is recognized as valid.

    test_title_is_required():
        Test that the form is invalid when the title field is empty.

    test_category_is_required():
        Test that the form is invalid when the category field is empty.

    test_cooking_time_is_required():
        Test that the form is invalid when the cooking time field is empty.

    test_servings_is_required():
        Test that the form is invalid when the servings field is empty.

    test_make_public_is_required():
        Test that the form is invalid when the make_public field is empty.
    """

    def test_form_is_valid(self):
        """
        Test that a RecipeForm with all required fields filled is considered
        valid.

        This test verifies that when a RecipeForm is provided with valid data,
        specifically non-empty 'title', 'category', 'cooking_duration',
        'servings', and 'make_public' fields, the form's is_valid() method
        returns True.
        """
        recipe_form = RecipeForm(
            {
                "title": "test",
                "category": "1",
                "cooking_duration": "20",
                "servings": "2",
                "make_public": "True",
                "recipe_image": "",
            }
        )
        self.assertTrue(recipe_form.is_valid(), msg="Form is not valid")

    def test_title_is_required(self):
        """
        Test that a RecipeForm without a title is considered invalid.

        This test checks that when a RecipeForm is provided with an empty
        'title' field, the form's is_valid() method returns False.
        """
        recipe_form = RecipeForm({"title": ""})
        self.assertFalse(recipe_form.is_valid(), msg="Form is not valid")

    def test_category_is_required(self):
        """
        Test that a RecipeForm without a category is considered invalid.

        This test checks that when a RecipeForm is provided with an empty
        'category' field, the form's is_valid() method returns False.
        """
        recipe_form = RecipeForm({"category": ""})
        self.assertFalse(recipe_form.is_valid(), msg="Form is not valid")

    def test_cooking_time_is_required(self):
        """
        Test that a RecipeForm without a cooking time is considered invalid.

        This test checks that when a RecipeForm is provided with an empty
        'cooking_time' field, the form's is_valid() method returns False.
        """
        recipe_form = RecipeForm({"cooking_time": ""})
        self.assertFalse(recipe_form.is_valid(), msg="Form is not valid")

    def test_servings_is_required(self):
        """
        Test that a RecipeForm without a servings field is considered invalid.

        This test checks that when a RecipeForm is provided with an empty
        'servings' field, the form's is_valid() method returns False.
        """
        recipe_form = RecipeForm({"servings": ""})
        self.assertFalse(recipe_form.is_valid(), msg="Form is not valid")

    def test_make_public_is_required(self):
        """
        Test that a RecipeForm without a make_public field is considered
        invalid.

        This test checks that when a RecipeForm is provided with an empty
        'make_public' field, the form's is_valid() method returns False.
        """
        recipe_form = RecipeForm({"make_public": ""})
        self.assertFalse(recipe_form.is_valid(), msg="Form is not valid")
