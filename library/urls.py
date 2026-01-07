from django.urls import path
from . import views

urlpatterns = [
    path("books/", views.books_list, name="books_list"),
    path("categories/", views.categories_list, name="categories_list"),
    path('mybooks/', views.mybooks, name='mybooks'),

]
