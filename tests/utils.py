from datetime import datetime

from django.contrib.auth.models import User

from api.serializers import ArticleSerializer, TagSerializer, UserSerializer
from django_articles.models import Article, Tag


def create_user(name: str, password: str) -> User:
    """
    Creates an Author model object.
    """
    return User.objects.create_user(username=name, email=f'{name}@example.com', password=password)


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


def serialize_article_with_absolute_urls(article: Article):
    serialized_article = ArticleSerializer(article, context={'request': None}).data
    serialized_article['url'] = f'http://testserver{serialized_article["url"]}'
    serialized_article['author'] = f'http://testserver{serialized_article["author"]}'
    serialized_article['tags'] = [f'http://testserver{tag}' for tag in serialized_article['tags']]
    return serialized_article


def serialize_user_with_absolute_urls(user: User):
    serialized_user = UserSerializer(user, context={'request': None}).data
    serialized_user['url'] = f'http://testserver{serialized_user["url"]}'
    serialized_user['articles'] = [f'http://testserver{article}' for article in serialized_user['articles']]
    return serialized_user


def serialize_tag_with_absolute_urls(tag: Tag):
    serialized_tag = TagSerializer(tag, context={'request': None}).data
    serialized_tag['url'] = f'http://testserver{serialized_tag["url"]}'
    serialized_tag['articles'] = [f'http://testserver{article}' for article in serialized_tag['articles']]
    return serialized_tag
