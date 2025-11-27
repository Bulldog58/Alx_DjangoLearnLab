# relationship_app/models.py
from django.db import models

class Author(models.Model):
    """
    Model for the Author. One Author to Many Books.
    """
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Book(models.Model):
    """
    Model for the Book. Contains the ForeignKey to Author.
    """
    title = models.CharField(max_length=200)
    
    # 🔑 ForeignKey (One-to-Many): A Book must have one Author.
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE, 
        related_name='books' # Allows querying author.books.all()
    )
    
    def __str__(self):
        return self.title

class Library(models.Model):
    """
    Model for the Library. Participates in ManyToMany (Books) and OneToOne (Librarian).
    """
    name = models.CharField(max_length=100)
    
    # 📚 ManyToManyField: Links to Book. A Library has many Books, a Book is in many Libraries.
    books = models.ManyToManyField(Book, related_name='libraries')
    
    def __str__(self):
        return self.name

class Librarian(models.Model):
    """
    Model for the Librarian. Contains the OneToOneField to Library.
    """
    name = models.CharField(max_length=100)
    
    # 👤 OneToOneField: Links to Library. Ensures one Librarian per Library.
    library = models.OneToOneField(
        Library, 
        on_delete=models.CASCADE, 
        primary_key=True # Makes Librarian's primary key the same as the Library's primary key
    )
    
    def __str__(self):
        return f"{self.name} ({self.library.name})"