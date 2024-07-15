from django.test import TestCase
from django.urls import reverse

from .forms import ReachOutForm
from .models import Contact


class TestContactView(TestCase):
    """
    Test suite for the ContactView.

    This class contains unit tests to ensure the ContactView behaves correctly
    by rendering the contact page with the appropriate content and handling
    the submission of the ReachOutForm.

    Methods:
    --------
    setUp():
        Set up the test contact content for use in the tests.

    test_render_contact_me_page_with_reachout_form():
        Test that the contact page is rendered correctly and contains the
        ReachOutForm.

    test_successful_reachout_submission():
        Test that a valid submission of the ReachOutForm is processed
        successfully and the appropriate response is returned.
    """

    def setUp(self):
        """
        Set up the test contact content.

        This method creates an instance of the Contact model with the title and
        content for the contact page and saves it to the database.
        """
        self.contact_content = Contact(
            title="Welcome,", content="Feel free to reach out"
        )
        self.contact_content.save()

    def test_render_contact_me_page_with_reachout_form(self):
        """
        Test that the contact page is rendered correctly and contains the
        ReachOutForm.

        This test sends a GET request to the contact page URL and checks that
        the response status code is 200 (OK), that the response content
        includes the title "Welcome", and that the response context contains an
        instance of the ReachOutForm.
        """
        response = self.client.get(reverse("contact"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome", response.content)
        self.assertIsInstance(response.context["reachout_form"], ReachOutForm)

    def test_successful_reachout_submission(self):
        """
        Test that a valid submission of the ReachOutForm is processed
        successfully and the appropriate response is returned.

        This test sends a POST request to the contact page URL with valid form
        data and checks that the response status code is 200 (OK) and that the
        response content includes the message "Thank you for reaching out".
        """
        post_data = {
            "name": "test name",
            "email": "test@email.com",
            "message": "test message",
        }
        response = self.client.post(reverse("contact"), post_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Thank you for reaching out,", response.content)
