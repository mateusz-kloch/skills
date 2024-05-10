# SKILLS

## A platform to share knowledge!
This platform was developed with Django and Django REST framework to let people share and expand their knowledge. Users can read articles as guests or can register to create their own articles.

### Repository layout:
```
├── skills_backend
│   ├── api
│   │   ├── __init__.py
│   │   ├── permissions.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── core
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── library
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── templates
│   │   └── library
│   │       ├── article_detail.html
│   │       ├── article_list.html
│   │       ├── author_detail.html
│   │       ├── author_list.html
│   │       ├── index.html
│   │       ├── tag_list.html
│   │       └── tag_relations_list.html
│   ├── tests
│   │   ├── __init__.py
│   │   ├── test_api_articles_endpoints.py
│   │   ├── test_api_root.py
│   │   ├── test_api_tags_endpoints.py
│   │   ├── test_api_users_endpoints.py
│   │   ├── test_library_models.py
│   │   ├── test_library_views.py
│   │   └── utils.py
│   ├── LICENSE
│   ├── manage.py
│   ├── README.md
│   └── requirements.txt
```
