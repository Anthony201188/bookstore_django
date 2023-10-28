"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from books.views import (
    BookListView,
    BookDetailView,
    BookUpdateView,
    BookCreateView,
    BookDeleteView,
    BookSelectView,
    BookUpdateConfirmView

)

urlpatterns = [
    path('', BookListView.as_view(), name='book-list'), # list view used as home
    path('detail/<int:pk>/', BookDetailView.as_view(), name='book-detail'), # rember that to pass the primary key to the url here using <int:pk>
    path('create/', BookCreateView.as_view() ,name='book-create'),
    path('update/', BookUpdateView.as_view(), name='book-update'),
    path('update/confirm/<int:pk>/', BookUpdateConfirmView.as_view(), name='book-update-confirm'),
    path('delete/<int:pk>/',BookDeleteView.as_view(), name='book-delete'),
    path('select/',BookSelectView.as_view(), name='book-select')
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)