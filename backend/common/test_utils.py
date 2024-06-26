from datetime import datetime

from api.serializers import ArticleSerializer, AuthorSerializer, TagSerializer
from library.models import Article, Author, Tag


def create_author(user_name: str, password: str) -> Author:
    """
    Creates an Author model object.
    Sets author.email as: `f'{user_name}@ex.com'` and
    `is_active=True`.
    """
    author = Author.objects.create_user(
        user_name=user_name, email=f'{user_name}@ex.com', password=password
    )
    author.is_active = True
    author.save()
    return author

def create_superuser(user_name:str, password: str) -> Author:
    """
    Creates an Author model supeuser object.
    Sets superuser.email as: `f'{user_name}@ex.com'`.
    """
    superuser = Author.objects.create_superuser(
        user_name=user_name, email=f'{user_name}@ex.com', password=password
    )
    superuser.save()
    return superuser

def create_tag(name: str) -> Tag:
    """
    Creates a Tag model object.
    """
    return Tag.objects.create(name=name)

def create_article(
        title: str, author: Author, pub_date: datetime|None, tags: list[Tag], content: str
    ) -> Article:
    """
    Creates an article model object and establishes a many-to-many relation with
    the given Tag objects.
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

def serialize_article(article: Article) -> dict:
    """
    Serializes Article model object and
    creates absolute urls for hyperlinked relations.
    """
    serialized_article = ArticleSerializer(article, context={'request': None}).data
    serialized_article['url'] = f'http://testserver{serialized_article["url"]}'
    serialized_article['author'] = f'http://testserver{serialized_article["author"]}'
    serialized_article['tags'] = [f'http://testserver{tag}' for tag in serialized_article['tags']]
    return serialized_article

def serialize_author(author: Author) -> dict:
    """
    Serializes Author model object and
    creates absolute urls for hyperlinked relations.
    """
    serialized_author = AuthorSerializer(author, context={'request': None}).data
    serialized_author['url'] = f'http://testserver{serialized_author["url"]}'
    serialized_author['avatar'] = f'http://testserver{serialized_author["avatar"]}'
    serialized_author['articles'] = [f'http://testserver{article}' for article in serialized_author['articles']]
    return serialized_author

def serialize_tag(tag: Tag) -> dict:
    """
    Serializes Tag model object and
    creates absolute urls for hyperlinked relations.
    """
    serialized_tag = TagSerializer(tag, context={'request': None}).data
    serialized_tag['url'] = f'http://testserver{serialized_tag["url"]}'
    serialized_tag['articles'] = [f'http://testserver{article}' for article in serialized_tag['articles']]
    return serialized_tag
