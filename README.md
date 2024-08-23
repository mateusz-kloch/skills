# SKILLS



## A platform to share knowledge!
**This blog platform consists both Django app and Django REST Framework API service.**



## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Repository tree](#repository-tree)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)



## Introduction

This project is a server Django application and API for blog. It allows users to register themselves and to create, update and delete their posts and to read other users posts.



## Features

- User authentication and authorization
- CRUD operations for posts
- Pagination for posts



## Repository tree
```
├── backend
│   ├── api
│   │   ├── permissions.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── common
│   │   └── test_utils.py
│   ├── core
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── library
│   │   ├── migrations
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── managers.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── static
│   │   ├── library
│   │   │   └── author
│   │   │       └── default
│   │   │           └── default_avatar.png
│   ├── templates
│   │   └── library
│   │       ├── article_detail.html
│   │       ├── article_list.html
│   │       ├── author_detail.html
│   │       ├── author_list.html
│   │       ├── index.html
│   │       ├── tag_detail.html
│   │       └── tag_list.html
│   ├── tests
│   │   ├── test_api_endpoints.py
│   │   ├── test_for_test_utils.py
│   │   ├── test_library_models.py
│   │   └── test_library_views.py
│   ├── .gitignore
│   ├── LICENSE
│   ├── manage.py
│   └── requirements.txt
└── README.md
```



## Installation

1. **Clone the repository:**

    ```bash

    git clone https://github.com/mateusz-kloch/skills.git

    cd skills/backend

    ```

2. **Create a virtual environment:**

    ```bash

    python3 -m venv venv

    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

    ```

3. **Install the dependencies:**

    ```bash

    pip install -r requirements.txt

    ```

4. **Apply migrations:**

    ```bash

    python manage.py migrate

    ```

5. **Create a superuser:**

    ```bash

    python manage.py createsuperuser

    ```

6. **Run the development server:**

    ```bash

    python manage.py runserver

    ```



## Configuration

By default, the project uses SQLite. To use a different database, update the `DATABASES` setting in `settings.py`.



## Usage

- **Admin Panel:**

Access the Django admin panel at `http://127.0.0.1:8000/admin/` to manage users and posts.

- **API Documentation:**

Access the API documentation at `http://127.0.0.1:8000/api/schema/swagger-ui/`.

Yot can also download it at `http://127.0.0.1:8000/api/schema/`.



## API Endpoints

- **Articles:**

  - `GET /api/articles/` - List all posts

  - `POST /api/articles/` - Create a new post

  - `GET /api/articles/{slug}/` - Retrieve a post

  - `PUT /api/articles/{slug}/` - Update a post

  - `PATCH /api/articles/{slug}/` - Update a post

  - `DELETE /api/articles/{slug}/` - Delete a post
 
- **Authors:**

  - `GET /api/authors/` - List all authors

  - `POST /api/authors/` - Create an author

  - `GET /api/authors/{slug}/` - Retrieve an author

  - `PUT /api/authors/{slug}/` - Update an author

  - `PATCH /api/authors/{slug}/` - Update an author

  - `DELETE /api/authors/{slug}/` - Delete an author
 
- **Tags:**

  - `GET /api/tags/` - List all tags

  - `POST /api/tags/` - Create a tag

  - `GET /api/tags/{slug}/` - Retrieve a tag

  - `PUT /api/tags/{slug}/` - Update a tag

  - `PATCH /api/tags/{slug}/` - Update a tag

  - `DELETE /api/tags/{slug}/` - Delete a tag



## Testing

Run the tests using the following command:

```bash

python manage.py test

```



## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.

2. Create a new branch (`git checkout -b feature-branch`).

3. Make your changes.

4. Commit your changes (`git commit -m 'Add some feature'`).

5. Push to the branch (`git push origin feature-branch`).

6. Open a pull request.



## License

This project is licensed under the BSD 2-Clause License. See the [LICENSE](LICENSE) file for details.

A default avatar image by [raphaelsilva](https://pixabay.com/users/raphaelsilva-4702998/) comes from [pixabay](https://pixabay.com/).
