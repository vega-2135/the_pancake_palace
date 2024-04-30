from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from .forms import CommentForm
from .models import Recipe


class TestRecipeDetailView(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(
            username="myUsername",
            password="myPassword",
            email="test@test.com"
        )
        self.recipe = Recipe(
            title="Recipe title",
            author=self.user,
            slug="recipe-title",
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
        self.recipe.save()

    def test_render_post_detail_page_with_comment_form(self):
        response = self.client.get(reverse(
            'recipe_detail', args=['recipe-title']))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Recipe title", response.content)
        self.assertIsInstance(
            response.context['comment_form'], CommentForm)
        

    def test_successful_comment_submission(self):
        """Test for posting a comment on a post"""
        self.client.login(
            username="myUsername", password="myPassword")
        post_data = {
            'content': 'This is a test comment.'
        }
        response = self.client.post(reverse(
            'recipe_detail', args=['recipe-title']), post_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"This is a test comment.", response.content)
        
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

class TestShareRecipeView(TestCase, Client):

    def setUp(self):
        self.user = User.objects.create_superuser(
            username="myUsername", password="myPassword", email="test@test.com"
        )
        self.recipe = Recipe(
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
        self.recipe.save()
        

    def test_no_access_to_create_recipe_if_not_logged_in(self):
        response = self.client.get(reverse('share_recipe'))
        self.assertRedirects(response, '/accounts/login/?next=/share/')
      
    def test_authenticated_user_can_access_share_recipe_page(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user=user)
        response = self.client.get('/share/')
        self.assertContains(response, 'title')
        self.assertContains(response, 'cooking_duration')
        self.assertContains(response, 'servings')
        self.assertContains(response, 'category')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'share_recipe.html')
      
    def test_create_recipe(self):
        """Test for a user requesting a collaboration"""
        self.client.login(
            username="myUsername", password="myPassword")
        post_data = {
            'title': 'Recipe Title',
            'cooking_time': 10,
            'serves': 1,
            'ingredients': '1 cup flour, 1cup milk',
            'preparation':'Step 1: Mix all together.',
            'category': 1,
            'make_publik': 'True'
        }
        response = self.client.post('/share/', post_data)
        self.assertEqual(response.status_code, 200)



        

class TestEditRecipeView(TestCase, Client):

    def setUp(self):
        self.user = User.objects.create_superuser(
            username="myUsername", password="myPassword", email="test@test.com"
        )
        self.user1 = User.objects.create_superuser(
            username="myUsername2", password="myPassword2", 
            email="test@test2.com"
        )
        self.recipe = Recipe(
            title="Recipe title",
            author_id=1,
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
        self.recipe.save()

    def test_no_access_to_edit_recipe_if_not_logged_in_(self):
        response = self.client.get(reverse(
            'edit_recipe',
            kwargs={'slug': 'recipe-title'}
        ))
        self.assertRedirects(response, 
                             '/accounts/login/?next=/edit/recipe-title/')
        
    def test_user_is_not_author_redirect(self):
        user = User.objects.get(pk=2)
        self.client.force_login(user=user)
        response = self.client.get(reverse(
            'edit_recipe',
            kwargs={'slug': 'recipe-title'}
        ))
        self.assertEqual(response.status_code, 403)

    def test_authenticated_recipe_author_can_access_edit_recipe_page(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user=user)
        response = self.client.get(reverse(
            'edit_recipe',
            kwargs={'slug': 'recipe-title'}
        ))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'share_recipe.html')