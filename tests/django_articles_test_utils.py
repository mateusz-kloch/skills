from datetime import datetime

from django.contrib.auth.models import User

from django_articles.models import Article, Tag


def create_user(name: str) -> User:
    """
    Creates an Author model object.
    """
    username = name
    email = f'{name}@example.com'
    password = 'DjangoTest123'
    return User.objects.create_user(username=username, email=email, password=password)


def create_tag(name: str) -> Tag:
    """
    Creates a Tag model object.
    """
    return Tag.objects.create(name=name)


def create_article(title: str, author: User, tags: list[Tag], pub_date: datetime, content: str) -> Article:
    """
    Creates an article model object and establishes a many-to-many relation with the given Tag objects.
    """
    article = Article(
        title=title,
        author=author,
        pub_date=pub_date,
        content=content
    )
    article.save()
    article.tags.set(tags)
    return article
