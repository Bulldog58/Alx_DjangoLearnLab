# relationship_app/views.py

from django.shortcuts import render, redirect
from django.views import View 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login # <-- Add this import
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from .models import Book
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from .models import Book # Import the model
from django.http import HttpResponseForbidden # To handle permission denied messages

# Placeholder for listing books (usually requires login, but not a custom permission)
@login_required
def book_list(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/book_list.html', {'books': books})


# 1. Protect Create View with 'can_create'
@permission_required('relationship_app.can_create', raise_exception=True)
def add_book(request):
    # ... logic to handle form submission and saving new Book ...
    return render(request, 'relationship_app/book_form.html', {'form': BookForm()})


# 2. Protect Edit View with 'can_edit'
@permission_required('relationship_app.can_edit', raise_exception=True)
def edit_book(request, pk):
    # book = get_object_or_404(Book, pk=pk)
    # ... logic to handle form submission and updating Book ...
    return render(request, 'relationship_app/book_form.html', {'form': BookForm()})


# 3. Protect Delete View with 'can_delete'
@permission_required('relationship_app.can_delete', raise_exception=True)
def delete_book(request, pk):
    # book = get_object_or_404(Book, pk=pk)
    # ... logic to delete the Book ...
    return redirect('book-list')
    
    
# 4. Protect Detail View with 'can_view' (optional, but good for verification)
@permission_required('relationship_app.can_view', raise_exception=True)
def book_detail(request, pk):
    # book = get_object_or_404(Book, pk=pk)
    return render(request, 'relationship_app/book_detail.html', {'book': book})

# --- Views Secured with Custom Permissions ---

# 1. Add Book (Requires 'can_add_book' permission)
@permission_required('relationship_app.can_add_book', login_url='login')
def add_book(request):
    # In a real app, this would handle a form submission (POST) and rendering (GET)
    if request.method == 'POST':
        # Logic to process form and save the book
        return redirect('book-list')
    
    return render(request, 'relationship_app/book_form.html', {'action': 'Add'})


# 2. Edit Book (Requires 'can_change_book' permission)
@permission_required('relationship_app.can_change_book', login_url='login')
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    # In a real app, this would handle form submission and rendering
    if request.method == 'POST':
        # Logic to process form and update the book
        return redirect('book-detail', pk=book.pk)
        
    return render(request, 'relationship_app/book_form.html', {'action': 'Edit', 'book': book})


# 3. Delete Book (Requires 'can_delete_book' permission)
@permission_required('relationship_app.can_delete_book', login_url='login')
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    # Only allow POST request for deletion
    if request.method == 'POST':
        book.delete()
        return redirect('book-list')
        
    # Show confirmation template on GET request
    return render(request, 'relationship_app/book_confirm_delete.html', {'book': book})

def is_admin(user):
    # Check if the user is authenticated and has the 'Admin' role
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    # Check if the user is authenticated and has the 'Librarian' role
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    # Check if the user is authenticated and has the 'Member' role
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

# --- Role-Based Views ---

@user_passes_test(is_admin, login_url='login')
def admin_view(request):
    # Access granted only if is_admin(request.user) is True
    return render(request, 'relationship_app/admin_view.html', {'role': 'Admin'})

@user_passes_test(is_librarian, login_url='login')
def librarian_view(request):
    # Access granted only if is_librarian(request.user) is True
    return render(request, 'relationship_app/librarian_view.html', {'role': 'Librarian'})

@user_passes_test(is_member, login_url='login')
def member_view(request):
    # Access granted only if is_member(request.user) is True
    return render(request, 'relationship_app/member_view.html', {'role': 'Member'})

# --- Helper Functions for Role Checking ---

# 1. Registration View
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() # <-- Save the user object to a variable
            login(request, user) # <-- Log the user in immediately
            # Redirect them to the homepage or book list after successful login/registration
            return redirect('book-list') # Assuming 'book-list' is a valid name
    else:
        form = UserCreationForm()
        
    context = {'form': form}
    return render(request, 'relationship_app/register.html', context)


# ... (list_books and LibraryDetailView remain the same)


# 2. Function-Based View (list_books)
def list_books(request):
    # This is required because relationship_app/urls.py tries to import it.
    # Replace the placeholder with your actual logic later.
    return render(request, 'relationship_app/book_list.html', {'message': 'Book List View'})


# 3. Class-Based View (LibraryDetailView)
class LibraryDetailView(View):
    # This is required because relationship_app/urls.py tries to import it.
    # Replace the placeholder with your actual logic later.
    def get(self, request, pk):
        return render(request, 'relationship_app/book_detail.html', {'pk': pk, 'message': 'Book Detail View'})