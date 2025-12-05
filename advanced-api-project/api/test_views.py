from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import Book, Author
from django.contrib.auth.models import User


class BookAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")

        self.author = Author.objects.create(name="Test Author")

        self.book = Book.objects.create(
            title="Test Book", author=self.author, publication_year=2022
        )

    def test_create_book(self):
        url = reverse("book-list")
        data = {
            "title": "New Book",
            "author": self.author.id,
            "publication_year": 2023,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(Book.objects.get(title="New Book").author, self.author)

    def test_update_book(self):
        url = reverse("book-detail", args=[self.book.id])
        data = {
            "title": "Updated Book",
            "author": self.author.id,
            "publication_year": 2023,
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Book")

    def test_delete_book(self):
        url = reverse("book-detail", args=[self.book.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_filter_books(self):
        another_author = Author.objects.create(name="Another Author")
        Book.objects.create(
            title="Another Book", author=another_author, publication_year=2021
        )
        url = reverse("book-list") + "?author=" + str(another_author.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_books(self):
        url = reverse("book-list") + "?search=Test"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        url = reverse("book-list") + "?search=Test Author"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_order_books(self):
        another_author = Author.objects.create(name="Another Author")
        Book.objects.create(
            title="Another Book", author=another_author, publication_year=2021
        )
        url = reverse("book-list") + "?ordering=publication_year"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Another Book")