# SKILLS
## A platform to share knowledge!
### This platform was developed with Django and Django REST framework to let people share and expand their knowledge. User are allowed to read articles as guest or their can register themeselve to create their own articles.
#### Repository layout:
```
├── api
│   ├── __init__.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── django_articles
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── 0002_remove_article_date_published_article_pub_date.py
│   │   ├── 0003_author_article_author.py
│   │   ├── 0004_alter_article_author.py
│   │   ├── 0005_alter_author_options_remove_author_user_email_and_more.py
│   │   ├── 0006_alter_article_author_alter_article_options_and_more.py
│   │   ├── __init__.py
│   ├── models.py
│   ├── templates
│   │   └── django_articles
│   │       ├── article_detail.html
│   │       ├── article_index.html
│   │       ├── author_detail.html
│   │       ├── author_index.html
│   │       ├── tag_index.html
│   │       └── tag_relations_index.html
│   ├── urls.py
│   └── views.py
├── skills
│   ├── asgi.py
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
|── tests
|   ├── __init__.py
|   ├── test_api_articles_endpoint.py
|   ├── test_api_register_endpoint.py
|   ├── test_api_root.py
|   ├── test_api_tags_endpoint.py
|   ├── test_api_users_endpoint.py
|   ├── test_django_articles_models.py
|   ├── test_django_articles_views.py
|   └── utils.py
├── .gitignore
├── LICENSE
├── Pipfile
├── Pipfile.lock
├── README.md
├── db.sqlite3
└── manage.py
```
#### Tools used in development:
- python 3.11.6
- coverage 7.4.4
- django 5.0.4
- django-debug-toolbar 4.3.0
- djangorestframework 3.15.1
