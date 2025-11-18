import os
import django
import sys
# Note: Removed 'inspect' for simplification

# --- CRITICAL FIX: Add the project root to the system path ---
# This line gets the absolute path of the directory containing manage.py (one level up)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)
# -----------------------------------------------------------


# Set up Django environment
# NOTE: 'LibraryProject' below MUST match the name of your inner configuration directory
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian
from django.db.models import Count # This line is optional but harmless

print("--- 1. Setting up Sample Data ---")

# --- Create Instances for All Models ---
author_orwell, _ = Author.objects.get_or_create(name="George Orwell")
# ... (rest of the script continues) ...