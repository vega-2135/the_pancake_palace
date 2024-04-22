from django.test import TestCase
from .forms import ReachOutForm


class TestReachOutForm(TestCase):

    def test_form_is_valid(self):
        """ Test for all fields"""
        form = ReachOutForm({
            'name': 'test',
            'email': 'test@test.com',
            'message': 'Hello!'
        })
        self.assertTrue(form.is_valid(), msg="Form is not valid")

    def test_name_is_required(self):
        """ Test for all fields"""
        form = ReachOutForm({
            'name': '',
            'email': 'test@test.com',
            'message': 'Hello!'
        })
        self.assertFalse(form.is_valid(), msg="Name field is empty but the form is valid")

    def test_email_is_required(self):
        """ Test for all fields"""
        form = ReachOutForm({
            'name': 'test',
            'email': '',
            'message': 'Hello!'
        })
        self.assertFalse(form.is_valid(), msg="Email field is empty but the form is valid")

    def test_message_is_required(self):
        """ Test for all fields"""
        form = ReachOutForm({
            'name': 'test',
            'email': 'test@test.com',
            'message': ''
        })
        self.assertFalse(form.is_valid(), msg="Message field is empty but the form is valid")