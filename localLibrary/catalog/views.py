from tokenize import group
from urllib import request
from django.shortcuts import render
from django.views import generic
from .models import Book, Author, BookInstance, Genre
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django import template
import uuid

def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    # Доступные книги (статус = 'a')
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()  # Метод 'all()' применён по умолчанию.
    num_genre = Genre.objects.filter(name__exact='Tomsk').count()
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1
    is_librarian = request.user.groups.filter(name='Librarians').exists()

    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(
        request,
        'index.html',
        context={'num_books':num_books,'num_instances':num_instances,'num_instances_available':num_instances_available,'num_authors':num_authors, 'num_genre': num_genre, 'num_visits':num_visits},
    )

class BookListView(generic.ListView):
    model = Book
    paginate_by = 10

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10    

class AuthorDetailView(generic.DetailView):
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class LoanedUsersByBookListView(LoginRequiredMixin,generic.ListView):
    model = User
    template_name ='catalog/list_borrowed_users.html'
    paginate_by = 10
    
    def get_queryset(self):
        borrowed_books = BookInstance.objects.filter(status__exact='o').values_list('id', flat=True)
        print(BookInstance.objects.filter(status__exact='o').order_by('due_back'))
        print(User.objects.filter(bookinstance__in=borrowed_books))
        return User.objects.filter(bookinstance__in=borrowed_books)
        


