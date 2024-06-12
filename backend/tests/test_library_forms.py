from django.test import TestCase

from library.forms import UserRegisterForm

class LibraryFormsTests(TestCase):

    def setUp(self):
        self.data = {
            'user_name': 'newuser',
            'email': 'newuser@ex.com',
            'password': 'o48aq7go4378',
            'password2': 'o48aq7go4378'
        }

    def test_form_valid_data(self):
        """
        Checks whether form is valid when data is correct.
        """
        form = UserRegisterForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_user_name(self):
        """
        Checks whether form is valid when user_name is incorrect.
        """
        self.data['user_name'] = ''
        form = UserRegisterForm(data=self.data)
        self.assertFalse(form.is_valid())

    def test_form_invalid_email(self):
        """
        Checks whether form is valid when email is incorrect.
        """
        self.data['email'] = 'notemail'
        form = UserRegisterForm(data=self.data)
        self.assertFalse(form.is_valid())

    def test_form_passwords_not_match(self):
        """
        Checks whether form is valid when password not matches.
        """
        self.data['password'] = '84obg'
        form = UserRegisterForm(data=self.data)
        self.assertFalse(form.is_valid())
