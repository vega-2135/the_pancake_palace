from django.test import TestCase
from django.urls import reverse

from .models import About


class TestAboutView(TestCase):

    def setUp(self):
        """Creates about me content"""
        self.about_content = About(
            title="About The Pancake Palace", content="Welcome to The Pancake Palace,")
        self.about_content.save()
        
    def test_render_about_page(self):
        """Verifies get request for about me page"""
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'About The Pancake Palace', response.content)