from django.shortcuts import render
from django.views import generic
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # TODO ? dlaczego tu sie nic nie wyswietla???
        context['all_list'] = Book.objects.all()
        return context

    # # TODO
    def get_queryset(self):
        """Overwriting the method which in default returns the list of all the particular model's objects"""
        qs = super().get_queryset()
        return qs.order_by('id').reverse()[:5]
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
    paginate_by = 50
#     jak przechodzi się do następnych stron

class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = "author_detail.html"



