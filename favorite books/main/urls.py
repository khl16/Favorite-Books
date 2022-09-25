from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('user/register', views.create_user),
    path('user/login', views.login_user),
    path('books', views.all_books),
    path('books/create', views.books_create),
    path('books/<int:id>', views.one_book),
    path('books/<int:id>/unfavorite', views.books_unfavorite),
    path('books/<int:id>/favorite', views.books_addFavorite),
    path('books/<int:id>/update', views.books_update),
    path('books/<int:id>/delete', views.books_delete),
    path('user/logout', views.logout_user),
]