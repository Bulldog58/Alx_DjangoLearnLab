from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required
from django.http import Http404
from .models import Book
from .forms import ExampleForm  # Import the form

# View to list all books
@permission_required('bookshelf.can_view_book', raise_exception=True)
def book_list(request):
    books = Book.objects.all()  # Get all books from the database
    return render(request, 'bookshelf/book_list.html', {'books': books})

# View to create a new book using ExampleForm
@permission_required('bookshelf.can_create_book', raise_exception=True)
def create_book(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Process the form data and create a new book
            title = form.cleaned_data['title']
            author = form.cleaned_data['author']
            published_date = form.cleaned_data['published_date']
            isbn = form.cleaned_data['isbn']

            # Create the book
            Book.objects.create(
                title=title,
                author=author,
                published_date=published_date,
                isbn=isbn
            )
            return redirect('book_list')  # Redirect to the book list view
    else:
        form = ExampleForm()  # Initialize an empty form

    return render(request, 'bookshelf/create_book.html', {'form': form})

# View to edit a book using ExampleForm
@permission_required('bookshelf.can_edit_book', raise_exception=True)
def edit_book(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        raise Http404("Book not found")

    if request.method == 'POST':
        form = ExampleForm(request.POST, instance=book)
        if form.is_valid():
            form.save()  # Save the updated book
            return redirect('book_list')  # Redirect to the book list view
    else:
        form = ExampleForm(instance=book)  # Prepopulate the form with the book data

    return render(request, 'bookshelf/edit_book.html', {'form': form, 'book': book})

# View to delete a book
@permission_required('bookshelf.can_delete_book', raise_exception=True)
def delete_book(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        raise Http404("Book not found")

    book.delete()
    return redirect('book_list')  # Redirect to the book list view