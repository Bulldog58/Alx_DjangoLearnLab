# LibraryProject/urls.py

from django.contrib import admin
from django.urls import path, include  # <-- 1. Ensure 'include' is imported
# REMOVE: from . import views  <-- This line should be deleted or commented out

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 2. Use 'include' to link the relationship_app URLs
    # This assumes all your app views start with '/relationship/'
    path('relationship/', include('relationship_app.urls')), 
    
    # You might also include a root path if needed, e.g.:
    # path('', include('relationship_app.urls')), 
]