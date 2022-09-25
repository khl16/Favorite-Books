from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Book
import bcrypt

# Create your views here.
def index(request):
    return render(request, "index.html")

def create_user(request):
    if request.method == "POST":
        errors = User.objects.user_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/')

        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()

        user1 = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hashed_pw,
        )
        request.session['user_id'] = user1.id
        return redirect('/books')
    return redirect('/')

def all_books(request):
    if 'user_id' not in request.session:
        return redirect('/')
    this_user = User.objects.filter(id=request.session['user_id'])
    context = {
        'user': this_user[0],
        'all_books': Book.objects.all(),
    }
    return render(request, 'books.html', context)    

def login_user(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/')
        this_user = User.objects.filter(email=request.POST['email'])
        request.session['user_id'] = this_user[0].id
        return redirect('/books')
    return redirect('/')

def books_create(request):
    if request.method == "POST":
        errors = Book.objects.book_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/books')
        this_user = User.objects.get(id=request.session['user_id'])
        book = Book.objects.create(
            title = request.POST['title'],
            description = request.POST['description'],
            uploaded_by = this_user
        )
        this_user.liked_books.add(book)
        return redirect(f'/books/{book.id}')
    return redirect('/')

def one_book(request, id):
    context = {
        'all_books': Book.objects.get(id=id),
        'current_user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, "booksid.html", context)

def books_unfavorite(request, id):
    user = User.objects.get(id=request.session['user_id'])
    book = Book.objects.get(id=id)
    user.liked_books.remove(book)
    return redirect(f'/books/{id}')

def books_addFavorite(request, id):
    user = User.objects.get(id=request.session['user_id'])
    book = Book.objects.get(id=id)
    user.liked_books.add(book)
    return redirect('/books')

def books_update(request, id):
    errors = Book.objects.update_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect(f'/books/{id}')
    book = Book.objects.get(id=id)
    book.description = request.POST['description']
    book.save()
    return redirect('/books')
    
def books_delete(request, id):
    book = Book.objects.get(id=id)
    book.delete()
    return redirect('/books')

def logout_user(request):
    request.session.clear()
    return redirect('/')