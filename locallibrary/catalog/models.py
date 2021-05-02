import uuid
from datetime import date
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse


class Genre(models.Model):
    """A model representing a book genre."""
    name = models.CharField(max_length=200,
                            help_text='Wprowadz gatunek ksiazki (np."Romans")')

    def __str__(self):
        """ Create a string for representing the Genre Model object."""
        return self.name


class Language(models.Model):
    """A model representing a book language."""
    name = models.CharField(max_length=100,
                            help_text='Wprowadz jezyk ksiazki (np. "polski")')

    def __str__(self):
        """ Create a string for representing the Language Model object."""
        return self.name


class Book(models.Model):
    """A model representing the book (in general, not any particular copy."""
    title = models.CharField(max_length=200,
                             verbose_name='Tytuł')
    author = models.ManyToManyField('Author', help_text='Wybierz autora lub autorow ksiazki.',
                                    verbose_name='Autor')
    summary = models.TextField(max_length=1000,
                               help_text='Wprowadz krotki opis ksiazki',
                               verbose_name='Opis książki')

    # zastanawiam sie, czy nie warto by jednak zmienic ISBN na ManyToOneField
    # poniewaz jedna ksiazka moze miec wiele wydan, a kazde znich bedzie miec inny numer ISBN
    isbn_message = 'Wpisz same cyfry z numeru ISBN, powinno ich byc dokladnie 13.'
    isbn = models.IntegerField(
        'ISBN',
        validators=[MinValueValidator(limit_value=1000000000000, message=isbn_message),
                    MaxValueValidator(limit_value=9999999999999, message=isbn_message)],
        help_text='13-cyfrowy <a href="https://www.isbn-international.org/content/what-isbn">numer ISBN</a>')

    genre = models.ManyToManyField(Genre,
                                   help_text='Wybierz gatunek ksiazki.',
                                   verbose_name='Gatunek')

    DEFAULT_LANG_ID = 1
    language = models.ForeignKey(
        Language,
        help_text='Wybierz jezyk ksiazki.',
        verbose_name='Język',
        default=DEFAULT_LANG_ID,
        on_delete=models.SET_DEFAULT,
        # null=True,
    )
    # ?
    today = date.today()
    curr_year = today.year

    first_published = models.IntegerField(
        validators=[MaxValueValidator(limit_value=curr_year, message='Rok nie moze byc pozniejszy od biezacego.')],
        help_text='Wprowadz rok pierwszego oryginalnego wydania, z "-", jeśli p.n.e.',
        verbose_name='Rok pierwszego wydania'
    )

    def __str__(self):
        """ Create a string for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Create the absolute url of the object"""
        return reverse('book_detail', args=[str(self.id)])

    def display_author(self):
        return '; '.join(f'{author.surname}, {author.names}' for author in self.author.all()[:4])

    display_author.short_description = 'Autor'

    def display_genre(self):
        """Create a string for the Genre. Required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Gatunek'

    def display_language(self):
        return self.language

    display_language.short_description = 'Język'


class BookInstance(models.Model):
    """Model representing the copy of a book, which can be hired out to an user."""
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text='Unikalne ID dla kazdej ksiazki w calej księgarni.')
    book = models.ForeignKey(
        'Book',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Tytuł książki")
    # imprint = models.CharField(max_length=200)
    due_back = models.DateField(
        null=True,
        blank=True,
        verbose_name='Wypożyczona do')
    borrower = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Pożyczający')

    # ? Dlaczego akutrat krotka?
    LOAN_STATUS = (
        ('m', 'W trakcie renowacji'),  # m - maintenance
        ('o', 'Wypożyczona'),  # o - on loan
        ('a', 'Dostępna'),  # a - available
        ('r', 'Zarezerwowana'),  # r - reserved
    )
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='a',
        help_text='Dostepnosc ksiazki',
    )
    prolonged = models.BooleanField(default=False)

    class Meta:
        # ? poproszę o wiecej info na temat klasy w klasie
        ordering = ['due_back']
        permissions = (('can_mark_returned', 'Can set book as returned'),)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    def __str__(self):
        return f'{self.id} ({self.book.title})'


class Author(models.Model):
    """Model representing the author of a book/books."""
    # ? czy __repr__ w modelu jest dobrą praktyką?
    # ? Czytałam gdzieś, że o ile __str__ nie jest konieczne w Pythonie,
    # ? o tyle __repr__ tak, ale sama nigdy nie używałam
    # ? i maam dość mgliste pojęcie na ten temat.
    surname = models.CharField(
        max_length=100,
        help_text='Wprowadz nazwisko autora',
        verbose_name='Nazwisko')
    names = models.CharField(
        # TODO napiszę validator sprawdzający czy imię nie zawiera znaków specjalnych poza myslnikami
        max_length=200,
        help_text='Wprowadz imiona autora (bez dodatkowych znakow pomiedzy)',
        verbose_name='Imiona')

    date_of_birth = models.DateField(
        # TODO napisze funkcje sprawdzajaca czy data urodzenia autora była przynajmniej 7 lat temu
        # TODO nadpiszę wiadomość błędu, jak to zrobic bez pisania validatora?
        # validators=[],
        help_text='Wprowadz date urodzin autora  w formacie RRRR-MM-DD',
        verbose_name='Data urodzin',
        blank=True,
        null=True)

    date_of_death = models.DateField(
        # TODO napisze funkcje sprawdzajaca czy data smierci autora nie przypada po dzisiejszej
        # validators=[],
        help_text='Wprowadz date smierci autora w formacie RRRR-MM-DD',
        verbose_name='Data śmierci',
        blank=True,
        null=True)

    bio = models.TextField(
        help_text='Wprowadz krotki zyciorys i charakterystyke autora',
        verbose_name='Notka biograficzna',
        blank=True,
        null=True)

    class Meta:
        ordering = ['surname']

    def __str__(self):
        """ Create a string for representing an Author Model object."""
        return f'{self.surname}, {self.names}'

    def get_absolute_url(self):
        """Create the absolute url of the object"""
        return reverse('author_detail', args=[str(self.id)])


# intermedietary class enabling ManyToManyField classes inlines
class Role(models.Model):
    ROLES = (
        ('a', 'autor'),  # m - author
        ('e', 'edytor'),  # o - editor
        ('t', 'tłumacz'),  # a - translator
    )
    role_name = models.CharField(
        max_length=1,
        choices=ROLES,
        blank=True,
        default='a')

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE
    )

    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE
    )
