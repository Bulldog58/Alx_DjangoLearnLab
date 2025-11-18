from django.db import models

# 1. Author Model (The 'One' side of ForeignKey)
class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# 2. Book Model (The 'Many' side of ForeignKey, The 'Many' side of ManyToMany)
class Book(models.Model):
    title = models.CharField(max_length=200)
    
    # --- ForeignKey Relationship ---
    # One Author can write Many Books (Book has the ForeignKey)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# 3. Library Model (The 'Many' side of ManyToMany, The 'One' side of OneToOne)
class Library(models.Model):
    name = models.CharField(max_length=100)
    
    # --- ManyToManyField Relationship ---
    # A Library can have Many Books, and a Book can be in Many Libraries
    books = models.ManyToManyField(Book)

    def __str__(self):
        return self.name

# 4. Librarian Model (The 'Many' side of OneToOne)
class Librarian(models.Model):
    name = models.CharField(max_length=100)
    
    # --- OneToOneField Relationship ---
    # A Library can have only one Librarian, and a Librarian works for only one Library
    library = models.OneToOneField(Library, on_delete=models.CASCADE)

    def __str__(self):
        return self.name