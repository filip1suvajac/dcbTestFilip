from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("books/", views.books_list, name="books_list"),
    path("categories/", views.categories_list, name="categories_list"),
    path('mybooks/', views.mybooks, name='mybooks'),
    path("books/<int:pk>/", views.book_detail, name="book_detail"),
    path("logout/", views.logout_view, name="logout"),
    path("books/<int:pk>/love/", views.toggle_love, name="toggle_love"),
]
