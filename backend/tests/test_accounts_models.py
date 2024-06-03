"""
Tests for `accounts` app models.

Tests are tagged with the name of the model they concern.

Available tags:
- `author_model`

Usage:
`python manage.py test --tag={tag_name}`
"""
from django.test import tag, TestCase

from accounts.models import Author
from common.test_utils import create_author


class AccountsModelsTests(TestCase):

    def setUp(self):
        self.author = create_author('author', '48s5tb4w3')
        self.another_author = create_author('another_author', 'a49o7wg3qvf')
        self.yet_another_author = create_author('yet_another_author', 'aiuh3h347q')


# Tests for Author model:
    @tag('author_model')
    def test_author_str(self):
        """
        Checks whether __str__ displays author correctly.
        """
        self.assertEqual(self.author.user_name, str(self.author))

    @tag('author_model')
    def test_author_ordering(self):
        """
        CHecks whether authors are ordered by user_name.
        """
        self.assertQuerySetEqual(
            Author.objects.all(),
            [self.another_author, self.author, self.yet_another_author]
        )

    @tag('author_model')
    def test_author_default_joined(self):
        """
        Checks whether joined is provided by default.
        """
        self.assertTrue(self.author.joined)

    @tag('author_model')
    def test_author_default_slug(self):
        """
        Checks whether slug is provided by default.
        """
        self.assertTrue(self.author.slug)