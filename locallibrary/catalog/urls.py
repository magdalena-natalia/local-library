from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # Books
    path('books/', views.BookListView.as_view(), name='books'),
    # re_path(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'),
    # lub:
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('book/create/', views.BookCreate.as_view(),name='book_create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book_update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book_delete'),

    # BookInstances
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my_borrowed'),
    path('loaned_books/', views.AllLoanedBooksByUsersListView.as_view(), name='all_borrowed'),
    path('book-copy/renew/<uuid:pk>/', views.renew_book, name='renew_book'),
    path('book-instance/return/<uuid:pk>', views.BookInstanceReturn.as_view(), name='return_book'),

    # Authors
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author_detail'),
    path('author/create/', views.AuthorCreate.as_view(), name='author_create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author_update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author_delete'),

]
