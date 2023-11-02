#books.urls
from django.urls import path
from .views import BooksListAPI,BooksDetailAPI

urlpatterns=[
    path('<int:pk>/', BooksDetailAPI.as_view(), name="book-detail-api"),
    path('', BooksListAPI.as_view(), name="book-list-api")
]

