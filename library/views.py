from django.shortcuts import render
from .models import Category

def books_list(request):
    return render(request, "library/books_list.html")

def categories_list(request):
    return render(request, "library/categories_list.html")

def categories_list(request):
    categories = Category.objects.all()
    return render(
        request,
        "library/categories_list.html",
        {"active_tab": "categories", "categories": categories},
    )

from django.shortcuts import render

def mybooks(request):
    return render(request, "library/mybooks.html")
