from django.test import TestCase
from django.urls import reverse

from .models import About


class TestAboutView(TestCase):
    """
    Test suite for the AboutView.

    This class contains unit tests to ensure the AboutView behaves correctly
    by rendering the about page with the appropriate content.

    Methods:
    --------
    setUp():
        Set up the test about content for use in the tests.

    test_render_about_page():
        Test that the about page is rendered correctly and contains the
        expected content.
    """

    def setUp(self):
        """
        Set up the test about content.

        This method creates an instance of the About model with the title and
        content for the about page and saves it to the database.
        """
        """Creates about me content"""
        self.about_content = About(
            title="About The Pancake Palace",
            content="Welcome to The Pancake Palace,",
        )
        self.about_content.save()

    def test_render_about_page(self):
        """
        Test that the about page is rendered correctly and contains the
        expected content.

        This test sends a GET request to the about page URL and checks that the
        response status code is 200 (OK) and that the response content includes
        the title "About The Pancake Palace".
        """
        """Verifies get request for about me page"""
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"About The Pancake Palace", response.content)
