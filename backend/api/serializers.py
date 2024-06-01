from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from library.models import Article, Tag
from accounts.models import Author


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.HyperlinkedRelatedField(
        read_only=True, view_name='author-detail',
    )

    class Meta:
        model = Article
        fields = [
            'url', 'id', 'title', 'author', 'tags', 'pub_date', 'content'
        ]


class TagSerializer(serializers.HyperlinkedModelSerializer):
    articles = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name='article-detail'
    )

    class Meta:
        model = Tag
        fields = [
            'url', 'id', 'name', 'articles'
        ]


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    articles = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name='article-detail'
    )

    class Meta:
        model = Author
        fields = [
            'url', 'id', 'user_name', 'email', 'password', 'joined', 'articles'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_password(self, value):
        """
        Uses Django validate_password function to
        validate password given to serializer.
        """
        validate_password(value)
        return value
    
    def create(self, validated_data):
        """
        Creates user from validated data.
        """
        author = Author(**validated_data)
        author.set_password(validated_data['password'])
        author.save()
        return author
