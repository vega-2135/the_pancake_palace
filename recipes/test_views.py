from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .forms import CommentForm
from .models import Recipe


class TestRecipeDetailView(TestCase):
    """
    Test suite for the RecipeDetailView.

    This class contains unit tests to ensure the RecipeDetailView behaves
    correctly under various conditions, such as rendering the detail page with
    a comment form and handling comment submissions.

    Methods:
    --------
    setUp():
        Set up a test user and a test recipe for use in the tests.

    test_render_post_detail_page_with_comment_form():
        Test that the recipe detail page renders correctly with the comment
        form.

    test_successful_comment_submission():
        Test that a comment can be successfully submitted to the recipe detail
        page.
    """

    def setUp(self):
        """
        Set up a test user and a test recipe.

        This method creates a superuser and a recipe instance which are used
        in the subsequent tests. The recipe is saved to the database.
        """
        self.user = User.objects.create_superuser(
            username="myUsername", password="myPassword", email="test@test.com"
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
            approved=True,
        )
        self.recipe.save()

    def test_render_post_detail_page_with_comment_form(self):
        """
        Test that the recipe detail page renders correctly with the comment
        form.

        This test sends a GET request to the recipe detail page and checks that
        the response status code is 200 (OK), that the recipe title appears in
        the response content, and that the context contains an instance of
        CommentForm.
        """
        response = self.client.get(
            reverse("recipe_detail", args=["recipe-title"])
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Recipe title", response.content)
        self.assertIsInstance(response.context["comment_form"], CommentForm)

    def test_successful_comment_submission(self):
        """
        Test that a comment can be successfully submitted to the recipe detail
        page.

        This test logs in the test user, posts a comment to the recipe detail
        page, and checks that the response status code is 200 (OK) and that the
        comment appears in the response content.
        """
        self.client.login(username="myUsername", password="myPassword")
        post_data = {"content": "This is a test comment."}
        response = self.client.post(
            reverse("recipe_detail", args=["recipe-title"]), post_data
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"This is a test comment.", response.content)


class TestRecipeListView(TestCase, Client):
    """
    Test suite for the RecipeListView.

    This class contains unit tests to ensure the RecipeListView behaves correctly
    under various conditions, such as rendering the home page and displaying the
    correct queryset of recipes.

    Methods:
    --------
    setUp():
        Set up a test user and multiple test recipes for use in the tests.

    test_get_home_page():
        Test that the home page is rendered correctly.

    test_show_queryset():
        Test that the queryset contains only recipes with status=1 and
        approved=True.
    """

    def setUp(self):
        """
        Set up a test user and multiple test recipes.

        This method creates a superuser and three recipe instances which are
        used in the subsequent tests. The recipes have different status and
        approval values to test the filtering functionality.
        """
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
            approved=True,
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
            approved=True,
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
            approved=False,
        )
        self.recipe3.save()

    def test_get_home_page(self):
        """
        Test that the home page is rendered correctly.

        This test sends a GET request to the home page URL and checks that the
        response status code is 200 (OK) and that the correct template
        ('index.html') is used for rendering the page.
        """
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_show_queryset(self):
        """
        Test that the queryset contains only recipes with status=1 and
        approved=True.

        This test verifies that the queryset returned by filtering recipes with
        status=1 and approved=True matches the expected queryset which contains
        only the recipe with the title "Recipe1 title".
        """
        expected_qs = Recipe.objects.filter(title="Recipe1 title")
        test_qs = Recipe.objects.filter(status=1, approved=True).order_by(
            "-created_on"
        )
        self.assertQuerysetEqual(test_qs, expected_qs)


class TestShareRecipeView(TestCase, Client):
    """
    Test suite for the ShareRecipeView.

    This class contains unit tests to ensure the ShareRecipeView behaves
    correctly under various conditions, such as handling access permissions,
    rendering the share recipe page for authenticated users, and creating new
    recipes.

    Methods:
    --------
    setUp():
        Set up a test user and a test recipe for use in the tests.

    test_no_access_to_create_recipe_if_not_logged_in():
        Test that an unauthenticated user is redirected to the login page when
        trying to access the share recipe page.

    test_authenticated_user_can_access_share_recipe_page():
        Test that an authenticated user can access the share recipe page and
        that the correct fields are present in the response.

    test_create_recipe():
        Test that an authenticated user can successfully create a new recipe by
        posting valid data to the share recipe page.
    """

    def setUp(self):
        """
        Set up a test user and a test recipe.

        This method creates a superuser and a recipe instance which are used
        in the subsequent tests. The recipe is saved to the database.
        """
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
            approved=True,
        )
        self.recipe.save()

    def test_no_access_to_create_recipe_if_not_logged_in(self):
        """
        Test that an unauthenticated user is redirected to the login page when
        trying to access the share recipe page.

        This test sends a GET request to the share recipe URL without logging
        in and checks that the user is redirected to the login page with the
        next parameter set to the share recipe URL.
        """
        response = self.client.get(reverse("share_recipe"))
        self.assertRedirects(response, "/accounts/login/?next=/share/")

    def test_authenticated_user_can_access_share_recipe_page(self):
        """
        Test that an authenticated user can access the share recipe page and
        that the correct fields are present in the response.

        This test logs in the test user, sends a GET request to the share
        recipe URL, and checks that the response contains the expected fields
        (title, cooking_duration, servings, category), that the response status
        code is 200 (OK), and that the correct template ('share_recipe.html')
        is used for rendering the page.
        """
        user = User.objects.get(pk=1)
        self.client.force_login(user=user)
        response = self.client.get("/share/")
        self.assertContains(response, "title")
        self.assertContains(response, "cooking_duration")
        self.assertContains(response, "servings")
        self.assertContains(response, "category")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "share_recipe.html")

    def test_create_recipe(self):
        """
        Test that an authenticated user can successfully create a new recipe by
        posting valid data to the share recipe page.

        This test logs in the test user, posts valid recipe data to the share
        recipe URL, and checks that the response status code is 200 (OK).
        """
        self.client.login(username="myUsername", password="myPassword")
        post_data = {
            "title": "Recipe Title",
            "cooking_time": 10,
            "serves": 1,
            "ingredients": "1 cup flour, 1cup milk",
            "preparation": "Step 1: Mix all together.",
            "category": 1,
            "make_publik": "True",
        }
        response = self.client.post("/share/", post_data)
        self.assertEqual(response.status_code, 200)


class TestEditRecipeView(TestCase, Client):
    """
    Test suite for the EditRecipeView.

    This class contains unit tests to ensure the EditRecipeView behaves
    correctly under various conditions, such as handling access permissions for
    editing a recipe.

    Methods:
    --------
    setUp():
        Set up test users and a test recipe for use in the tests.

    test_no_access_to_edit_recipe_if_not_logged_in():
        Test that an unauthenticated user is redirected to the login page when
        trying to access the edit recipe page.

    test_user_is_not_author_redirect():
        Test that a user who is not the author of the recipe receives a 403
        Forbidden status when trying to access the edit recipe page.

    test_authenticated_recipe_author_can_access_edit_recipe_page():
        Test that an authenticated user who is the author of the recipe can
        access the edit recipe page.
    """

    def setUp(self):
        """
        Set up test users and a test recipe.

        This method creates two superusers and a recipe instance which are used
        in the subsequent tests. The recipe is saved to the database with one
        of the users as the author.
        """
        self.user = User.objects.create_superuser(
            username="myUsername", password="myPassword", email="test@test.com"
        )
        self.user1 = User.objects.create_superuser(
            username="myUsername2",
            password="myPassword2",
            email="test@test2.com",
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
            approved=True,
        )
        self.recipe.save()

    def test_no_access_to_edit_recipe_if_not_logged_in_(self):
        """
        Test that an unauthenticated user is redirected to the login page when
        trying to access the edit recipe page.

        This test sends a GET request to the edit recipe URL without logging in
        and checks that the user is redirected to the login page with the next
        parameter set to the edit recipe URL.
        """
        response = self.client.get(
            reverse("edit_recipe", kwargs={"slug": "recipe-title"})
        )
        self.assertRedirects(
            response, "/accounts/login/?next=/edit/recipe-title/"
        )

    def test_user_is_not_author_redirect(self):
        """
        Test that a user who is not the author of the recipe receives a 403
        Forbidden status when trying to access the edit recipe page.

        This test logs in a user who is not the author of the recipe, sends a
        GET request to the edit recipe URL, and checks that the response status
        code is 403 Forbidden.
        """
        user = User.objects.get(pk=2)
        self.client.force_login(user=user)
        response = self.client.get(
            reverse("edit_recipe", kwargs={"slug": "recipe-title"})
        )
        self.assertEqual(response.status_code, 403)

    def test_authenticated_recipe_author_can_access_edit_recipe_page(self):
        """
        Test that an authenticated user who is the author of the recipe can
        access the edit recipe page.

        This test logs in the user who is the author of the recipe, sends a GET
        request to the edit recipe URL, and checks that the response status
        code is 200 (OK) and that the correct template ('share_recipe.html') is
        used for rendering the page.
        """
        user = User.objects.get(pk=1)
        self.client.force_login(user=user)
        response = self.client.get(
            reverse("edit_recipe", kwargs={"slug": "recipe-title"})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "share_recipe.html")
