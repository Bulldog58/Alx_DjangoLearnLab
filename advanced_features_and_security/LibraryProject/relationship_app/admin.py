# advanced_features_and_security/relationship_app/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser # Import your custom user model
from .models import Book

admin.site.register(Book)
# Define the CustomUserAdmin class
class CustomUserAdmin(UserAdmin):
    # Add new fieldset for custom fields
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Profile Info', {'fields': ('date_of_birth', 'profile_photo')}),
    )
    
    # Optional: Add custom fields to the list view column
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_of_birth')

# Register the model with the custom admin class
admin.site.register(CustomUser, CustomUserAdmin)


# Unregister the default User model if it was ever registered
try:
    admin.site.unregister(CustomUser)
except admin.sites.NotRegistered:
    pass # Ignore if it was never registered

# Register your CustomUser model with the custom Admin class
admin.site.register(CustomUser, CustomUserAdmin)