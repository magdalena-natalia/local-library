from datetime import date, timedelta
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
# TODO czy często się robi tak jak w 2 poniższych liniach (podwójny import)?
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from catalog.forms import RenewBookForm, BookInstanceReturnForm, BookInstanceChangeStatusForm, BookInstanceBorrowForm, \
    BookInstanceReserveForm
from catalog.models import Author, Book, BookInstance, Genre


def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Dostępne książki (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # Funkcja 'all()' jest wykonywana domyślnie nawet jak nie jest stricte wywoływana.
    num_authors = Author.objects.count()  # to samo co -> Author.objects.all().count()

    num_genres = Genre.objects.count()
    # TODO ? kiedy stosować context jak nizej a kiedy get_context?
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
    }

    # Przekazywanie do wzorca html danych przy pomocy zmiennej context
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    template_name = 'book_list.html'
    paginate_by = 10

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['all_list'] = Book.objects.all()
    #     return context

    def get_queryset(self):
        """Overwriting the method which in default returns the list of all the particular model's objects"""
        qs = super().get_queryset()
        return qs.order_by('id').reverse()
        # order_by -'id'

        # return reversed(qs) # brak ksiazek w bibliotece
    #     #     # kiedy powinnam używać super w get_queryset?
    # #     # ? return 5 lastly added books
    # TODO próbowałam wszystkiego, ujemnego indeksowania, reverse; nie umiem
    # TODO nie umiem też wywołać get_queryset


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'book_detail.html'


class AuthorListView(generic.ListView):
    model = Author
    template_name = 'author_list.html'
    paginate_by = 10


#     jak przechodzi się do następnych stron

class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = "author_detail.html"


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'bookinstance_list_loaned_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class AllLoanedBooksByUsersListView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'bookinstance_list_loaned.html'
    permission_required = 'catalog.can_mark_returned'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.all().filter(status__exact='o').order_by('due_back')


@permission_required('catalog.can_mark_returned')
def renew_book(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)
    if request.method == 'POST':
        form = RenewBookForm(request.POST)
        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.prolonged = True
            book_instance.save()
            return HttpResponseRedirect(reverse('all_borrowed'))
    else:
        proposed_renewal_date = date.today() + timedelta(days=30)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})
    context = {
        'form': form,
        'book_instance': book_instance,
    }
    return render(request, 'book_renew.html', context)


class AuthorCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'catalog.add_author'
    template_name = 'author_form.html'
    model = Author
    fields = '__all__'
    success_url = reverse_lazy('authors')


class AuthorUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'catalog.change_author'
    template_name = 'author_form.html'
    model = Author
    fields = '__all__'
    # success_url = reverse_lazy('authors')


class AuthorDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = 'catalog.delete_author'
    template_name = 'author_confirm_delete.html'
    model = Author
    success_url = reverse_lazy('authors')


class BookCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'catalog.add_book'
    template_name = 'book_form.html'
    model = Book
    fields = '__all__'


class BookUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'catalog.change_book'
    template_name = 'book_form.html'
    model = Book
    fields = '__all__'


class BookDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = "catalog.delete_book"
    template_name = 'book_confirm_delete.html'
    model = Book
    success_url = reverse_lazy('books')


class BookInstanceReturn(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'catalog.can_mark_returned'
    template_name = 'bookinstance_form.html'
    model = BookInstance
    form_class = BookInstanceReturnForm
    success_url = reverse_lazy('all_borrowed')


class BookInstanceCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'catalog.add_bookinstance'
    template_name = 'bookinstance_form.html'
    model = BookInstance
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('book_detail', kwargs={'pk': self.kwargs.get("pk")})

    def get_initial(self):
        self.book = Book.objects.get(pk=self.kwargs.get("pk"))
        return {
            "status": "a",
            "book": self.book
        }


class BookInstanceUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'catalog.change_bookinstance'
    template_name = 'bookinstance_form.html'
    model = BookInstance
    fields = '__all__'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['book_title'] = self.kwargs.get('book_title')
        context['book_pk'] = self.kwargs.get('book_pk')
        context['pk'] = self.kwargs.get('pk')
        return context

    def get_success_url(self):
        return reverse_lazy('book_detail', kwargs={'pk': self.kwargs.get("book_pk")})


class BookInstanceDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = 'catalog.delete_book'
    template_name = 'bookinstance_confirm_delete.html'
    model = BookInstance

    # TODO Skąd wiesz, jakich kluczy użyć?
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['book_title'] = self.kwargs.get('book_title')
        context['book_pk'] = self.kwargs.get('book_pk')
        context['pk'] = self.kwargs.get('pk')
        return context

    def get_success_url(self):
        return reverse_lazy('book_detail', kwargs={'pk': self.kwargs.get("book_pk")})


class BookInstanceChangeStatus(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'catalog.can_mark_returned'
    template_name = 'bookinstance_form.html'
    model = BookInstance
    form_class = BookInstanceChangeStatusForm
    success_url = reverse_lazy('all_borrowed')
    initial = {'due_back': date.today() + timedelta(days=30)}

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        if form.cleaned_data['status'] == 'a' or form.cleaned_data['status'] == 'm':
            self.object.due_back = None
            self.object.borrower = None
            self.object.save()
        return super().form_valid(form)


class BookInstanceBorrow(LoginRequiredMixin, UpdateView):
    template_name = 'bookinstance_form.html'
    model = BookInstance
    form_class = BookInstanceBorrowForm
    success_url = reverse_lazy('my_borrowed')

    def get_initial(self):
        initial = super().get_initial()
        initial['status'] = 'o'
        initial['borrower'] = self.request.user
        initial['due_back'] = date.today() + timedelta(days=30)
        return initial


class BookInstanceReserve(LoginRequiredMixin, UpdateView):
    template_name = 'bookinstance_form.html'
    model = BookInstance
    form_class = BookInstanceReserveForm
    success_url = reverse_lazy('my_borrowed')

    def get_initial(self):
        initial = super().get_initial()
        initial['status'] = 'r'
        initial['borrower'] = self.request.user
        initial['due_back'] = date.today() + timedelta(days=30)
        return initial
