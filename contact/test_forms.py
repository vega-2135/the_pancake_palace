from django.test import TestCase

from .forms import ReachOutForm


class TestReachOutForm(TestCase):
    """
    Test suite for the ReachOutForm.

    This class contains unit tests to ensure the ReachOutForm behaves correctly
    by validating the presence and correctness of the required fields: name,
    email, and message.

    Methods:
    --------
    test_form_is_valid():
        Test that the form is valid when all fields are correctly filled.

    test_name_is_required():
        Test that the form is invalid when the name field is empty.

    test_email_is_required():
        Test that the form is invalid when the email field is empty.

    test_message_is_required():
        Test that the form is invalid when the message field is empty.
    """

    def test_form_is_valid(self):
        """
        Test that the form is valid when all fields are correctly filled.

        This test case checks if the form is valid when all required fields
        (name, email, message) are provided with valid data.
        """
        form = ReachOutForm(
            {"name": "test", "email": "test@test.com", "message": "Hello!"}
        )
        self.assertTrue(form.is_valid(), msg="Form is not valid")

    def test_name_is_required(self):
        """
        Test that the form is invalid when the name field is empty.

        This test case checks if the form is invalid when the name field
        is left empty, ensuring that the name field is required.
        """
        form = ReachOutForm(
            {"name": "", "email": "test@test.com", "message": "Hello!"}
        )
        self.assertFalse(
            form.is_valid(), msg="Name field is empty but the form is valid"
        )

    def test_email_is_required(self):
        """
        Test that the form is invalid when the email field is empty.

        This test case checks if the form is invalid when the email field
        is left empty, ensuring that the email field is required.
        """
        form = ReachOutForm({"name": "test", "email": "", "message": "Hello!"})
        self.assertFalse(
            form.is_valid(), msg="Email field is empty but the form is valid"
        )

    def test_message_is_required(self):
        """
        Test that the form is invalid when the message field is empty.

        This test case checks if the form is invalid when the message field
        is left empty, ensuring that the message field is required.
        """
        form = ReachOutForm(
            {"name": "test", "email": "test@test.com", "message": ""}
        )
        self.assertFalse(
            form.is_valid(),
            msg="Message field is empty but the form is valid",
        )
