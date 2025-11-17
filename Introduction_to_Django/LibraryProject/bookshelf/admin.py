from django.contrib import admin
from .models import Book

# --- Customize the Admin Interface ---
class BookAdmin(admin.ModelAdmin):
    # 1. Customize the List View Display: fields shown on the main table
    list_display = ('title', 'author', 'publication_year')

    # 2. Configure List Filters: sidebar filters for quick sorting
    list_filter = ('author', 'publication_year')

    # 3. Configure Search Capabilities: fields searchable via the admin search box
    search_fields = ('title', 'author', 'publication_year')

    # Optional: Fields to make clickable links to the edit page
    list_display_links = ('title',)

# Register the Book Model with the Django Admin
admin.site.register(Book, BookAdmin)