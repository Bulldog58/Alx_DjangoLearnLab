Advanced API Project
Welcome to the Advanced API Project! This project is built using Django and Django REST Framework to create a powerful API that can be used for various applications.

Table of Contents
Advanced API Project
Table of Contents
Getting Started
Prerequisites
Installation
Project Structure
Filtering, Searching, and Ordering
Filtering:
Searching:
Ordering:
Getting Started
Follow the steps below to set up your development environment and get started with the project.

Prerequisites
Make sure you have Python and pip installed on your machine.

Installation
Activate your Virtual Environment
Create and activate your virtual environment to keep your project dependencies isolated:

python -m venv djenv used to create the virtual environment named djenv

On Windows use djenv\Scripts\activate to activate the virtual environment

Install Required Packages
Install Django and Django REST Framework by running:

pip install django djangorestframework

Create the Django Project
Start a new Django project:

django-admin startproject advanced_api_project .

Navigate to the Project Directory
Change into the project directory:

cd advanced_api_project

Create a Django App
Create a new Django app named api:

django-admin startapp api

Project Structure
Here’s a brief overview of the project structure:

advanced_api_project/
│
├── api/                     # Your API application
│   ├── migrations/          # Database migrations
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
│
├── advanced_api_project/    # Main project directory
│   ├── __init__.py
|   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
└── manage.py                # Project management script
└── README.md
Filtering, Searching, and Ordering
The following features are available on the /api/books/ endpoint:

Filtering:
You can filter books by the following fields:
title: Filter by book title.
author: Filter by book author.
publication_year: Filter by the year the book was published.
Example:GET /api/books/?title=Book Title&author=Author Name&publication_year=2022

Searching:
You can search for books by title or author.
Example:GET /api/books/?search=book

Ordering:
You can order the results by title or publication_year.
Example:GET /api/books/?ordering=title

We can also combine filtering, searching, and ordering in a single query:

GET /api/books/?author=Author Name&search=book&ordering=publication_year

