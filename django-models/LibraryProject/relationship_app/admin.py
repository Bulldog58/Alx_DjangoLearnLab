from django.contrib import admin
from .models import Author, Book, Library, Librarian # Import ALL the models

# Register the models to make them visible in the Django Admin
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Library)
admin.site.register(Librarian)