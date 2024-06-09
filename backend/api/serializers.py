from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from library.models import Article, Author, Tag


class ArticleSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ['author', 'slug']
        extra_kwargs = {
            'url': {'lookup_field': 'slug'},
            'author': {
                'lookup_field': 'slug',
                'read_only': True,
            },
            'slug': {'read_only': True},
            'tags': {'lookup_field': 'slug'},
        }
    
    def create(self, validated_data):
        """
        Creates Article object from validated data.
        Assings User who create article as author of it.
        """
        author = self.context['request'].user
        validated_data['author'] = author
        tags = validated_data.pop('tags', None)
        article = Article(**validated_data)
        article.save()
        article.tags.set(tags)
        return article


class AuthorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Author
        fields = ['url', 'user_name', 'slug', 'email', 'avatar', 'joined', 'password', 'articles']
        extra_kwargs = {
            'url': {'lookup_field': 'slug'},
            'slug': {'read_only': True},
            'joined': {'read_only': True},
            'password': {'write_only': True},
            'articles': {
                'lookup_field': 'slug',
                'read_only': True,
                },
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


class TagSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Tag
        fields = ['url', 'name', 'slug', 'articles']
        extra_kwargs = {
            'url': {'lookup_field': 'slug'},
            'slug': {'read_only': True},
            'articles': {
                'lookup_field': 'slug',
                'read_only': True,
                },
        }
