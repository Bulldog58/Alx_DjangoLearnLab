### 3. `update.md` (Update Operation)

```markdown
# Update Operation Documentation

**Objective:** Update the title of “1984” to “Nineteen Eighty-Four” and save the changes.

**Shell Command:**
```python
>>> from bookshelf.models import Book
>>> book_to_update = Book.objects.get(title="1984")
>>> book_to_update.title = "Nineteen Eighty-Four"
>>> book_to_update.save()
>>> # Confirm the update by retrieving the new title:
>>> Book.objects.get(author="George Orwell").title