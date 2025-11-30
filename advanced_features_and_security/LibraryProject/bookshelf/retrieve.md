### 2. `retrieve.md` (Retrieve Operation)

```markdown
# Retrieve Operation Documentation

**Objective:** Retrieve and display all attributes of the book just created.

**Shell Command:**
```python
>>> from bookshelf.models import Book
>>> retrieved_book = Book.objects.get(title="1984")
>>> print(f"Title: {retrieved_book.title}, Author: {retrieved_book.author}, Year: {retrieved_book.publication_year}")