# SKILLS

## A platform to share knowledge!
This platform was developed with Django and Django REST framework to let people share and expand their knowledge. Users can read articles as guests or can register to create their own articles.

### Tools used in development:
- python
- coverage
- django
- django-cors-headers
- django-debug-toolbar
- djangorestframework

:memo: Tool versions are specified in the `requirements.txt` file.

### Repository layout:
```
├── core
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── library
│   ├── api
│   │   ├── __init__.py
│   │   ├── permissions.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── templates
│   │   └── library
│   │       ├── article_detail.html
│   │       ├── article_index.html
│   │       ├── author_detail.html
│   │       ├── author_index.html
│   │       ├── index.html
│   │       ├── tag_index.html
│   │       └── tag_relations_index.html
│   |── tests
│   |   ├── __init__.py
│   |   ├── test_api_articles_endpoint.py
│   |   ├── test_api_register_endpoint.py
│   |   ├── test_api_root.py
│   |   ├── test_api_tags_endpoint.py
│   |   ├── test_api_users_endpoint.py
│   |   ├── test_library_models.py
│   |   ├── test_library_views.py
│   |   └── utils.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── .gitignore
├── LICENSE
├── manage.py
├── README.md
└── requirements.txt
```