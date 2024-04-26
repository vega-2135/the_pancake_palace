from django.contrib.auth.models import User
from django.test import Client, TestCase

from .models import Recipe


class TestRecipeListView(TestCase, Client):

    def setUp(self):
        self.user = User.objects.create_superuser(
            username="myUsername", password="myPassword", email="test@test.com"
        )
        self.recipe1 = Recipe(
            title="Recipe1 title",
            author=self.user,
            slug="recipe1-title",
            category=1,
            ingredients="1 cup flour, 1 cup milk",
            preparation="Step 1: Mix all together.",
            cooking_duration=20,
            servings=2,
            make_public="True",
            recipe_image="",
            status=1,
            approved=True
        )
        self.recipe1.save()
        
        self.recipe2 = Recipe(
            title="Recipe2 title",
            author=self.user,
            slug="recipe2-title",
            category=1,
            ingredients="1 cup flour, 1 cup milk",
            preparation="Step 1: Mix all together.",
            cooking_duration=20,
            servings=2,
            make_public="True",
            recipe_image="",
            status=0,
            approved=True
        )
        self.recipe2.save()
        
        self.recipe3 = Recipe(
            title="Recipe3 title",
            author=self.user,
            slug="recipe3-title",
            category=1,
            ingredients="1 cup flour, 1 cup milk",
            preparation="Step 1: Mix all together.",
            cooking_duration=20,
            servings=2,
            make_public="True",
            recipe_image="",
            status=1,
            approved=False
        )
        self.recipe3.save()
   
    def test_get_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_show_queryset(self):
        expected_qs = Recipe.objects.filter(title="Recipe1 title")
        test_qs = Recipe.objects.filter(
            status=1,
            approved=True
        ).order_by('-created_on')
        self.assertQuerysetEqual(test_qs, expected_qs)


