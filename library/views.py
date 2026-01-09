from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Book
from django.views.decorators.http import require_POST,require_http_methods
from django.http import JsonResponse
from django.db.models.deletion import ProtectedError
from django.urls import reverse



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
    categories = Category.objects.all()
    return render(request, "library/books_list.html", {"books": books, "categories": categories})

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


@require_POST
@login_required_custom
def category_create(request):
    name = (request.POST.get("name") or "").strip()
    if not name:
        return JsonResponse({"ok": False, "error": "Missing name"}, status=400)

    obj, created = Category.objects.get_or_create(name=name)
    if not created:
        return JsonResponse({"ok": False, "error": "Category already exists"}, status=400)

    return JsonResponse({
        "ok": True,
        "id": obj.id,
        "name": obj.name,
        "book_count": 0,
    })


@require_POST
@login_required_custom
def category_delete(request, pk):
    cat = get_object_or_404(Category, pk=pk)
    try:
        cat.delete()
    except ProtectedError:
        return JsonResponse(
            {"ok": False, "error": "Canont delete category, because a book exists within this category."},
            status=400
        )
    return JsonResponse({"ok": True})

@require_POST
@login_required_custom
def book_create(request):
    name = (request.POST.get("name") or "").strip()
    author = (request.POST.get("author") or "").strip()
    desc = (request.POST.get("desc") or "").strip()
    year = request.POST.get("year")
    rating = request.POST.get("rating") 
    category_id = request.POST.get("category_id")

    if not name or not author or not desc or not rating or not year or not category_id:
        return JsonResponse({"ok": False, "error": "Missing fields"}, status=400)

    category = get_object_or_404(Category, pk=category_id)

    b = Book.objects.create(
        name=name,
        author=author,
        desc=desc,
        year=int(year),
        rating=int(rating) if rating else None,
        category=category,
    )

    return JsonResponse({
        "ok": True,
        "id": b.id,
        "name": b.name,
        "author": b.author,
        "category_name": b.category.name,
        "detail_url": f"/books/{b.id}/",
        "love_url": reverse("toggle_love", args=[b.id]),
        "edit_url": reverse("book_edit", args=[b.id]),
    })


@require_POST
@login_required_custom
def book_delete(request, pk):
    b = get_object_or_404(Book, pk=pk)
    b.delete()
    return JsonResponse({"ok": True})


@require_http_methods(["GET", "POST"])
@login_required_custom
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    categories = Category.objects.all()

    if request.method == "POST":
        book.name = request.POST.get("name", "").strip()
        book.author = request.POST.get("author", "").strip()
        book.year = int(request.POST.get("year") or 0)
        book.desc = request.POST.get("desc", "").strip()
        book.category = get_object_or_404(Category, pk=request.POST.get("category_id"))

        rating = (request.POST.get("rating") or "").strip()
        book.rating = int(rating) if rating else None

        book.save()
        return redirect("book_detail", pk=book.pk)

    return render(request, "library/book_edit.html", {
        "book": book,
        "categories": categories,
    })
