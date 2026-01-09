from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Book
from django.contrib.auth import logout
from django.views.decorators.http import require_POST

def login_required_custom(view):
    def wrapper(request, *args, **kwargs):
        if not request.session.get("logged_in"):
            return redirect("home")
        return view(request, *args, **kwargs)
    return wrapper

def logout_view(request):
    request.session.flush()
    return redirect("home")

@login_required_custom
def books_list(request):
    books = Book.objects.select_related("category").all()
    return render(request, "library/books_list.html", {"books": books})

@login_required_custom
def categories_list(request):
    categories = Category.objects.all()
    return render(request, "library/categories_list.html", {"categories": categories})

@login_required_custom
def mybooks(request):
    return render(request, "library/mybooks.html")

def home(request):
    correct_password = "test123"
    error = None

    if request.method == "POST":
        pw = request.POST.get("password")
        if pw == correct_password:
            request.session["logged_in"] = True
            return redirect("books_list")
        else:
            error = "Wrong password"

    return render(request, "library/home.html", {"error": error})

@login_required_custom
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, "library/book_detail.html", {"book": book})

@require_POST
@login_required_custom
def toggle_love(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.loved = not book.loved
    book.save()
    return redirect(request.META.get("HTTP_REFERER", "books_list"))

@login_required_custom
def mybooks(request):
    books = Book.objects.filter(loved=True)
    return render(request, "library/mybooks.html", {"books": books})
