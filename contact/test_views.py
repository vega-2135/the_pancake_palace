from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Contact
from .forms import ReachOutForm


class TestContactView(TestCase):

    def setUp(self):
        """Creates contact me content"""
        self.contact_content = Contact(
            title="Welcome,", content="Feel free to reach out")
        self.contact_content.save()

    def test_render_contact_me_page_with_reachout_form(self):
        """Verifies get request for contact me containing a reachout form"""
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome', response.content)
        self.assertIsInstance(
            response.context['reachout_form'], ReachOutForm)
        
    def test_successful_reachout_submission(self):
        """Test for a user reaching out"""
        post_data = {
            'name': 'test name',
            'email': 'test@email.com',
            'message': 'test message'
        }
        response = self.client.post(reverse('contact'), post_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b'Thank you for reaching out,', response.content)