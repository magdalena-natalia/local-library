from django.test import TestCase

from catalog.models import Author


class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Author.objects.create(surname='Big', names='Bob Gandalf')

    def test_surname_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('surname').verbose_name
        self.assertEquals(field_label, 'Nazwisko')

    def test_object_name_is_surname_comma_names(self):
        author = Author.objects.get(id=1)
        expected_object_name = f'{author.surname}, {author.names}'
        self.assertEquals(expected_object_name, str(author))

    def test_get_absolute_url(self):
        author = Author.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEquals(author.get_absolute_url(), '/catalog/author/1/')

    # TODO 1. Napisz test, który sprawdzi verbose_name pola date_of_death czy jest identyczny z frazą "Data śmierci'"
    # Podmieniłam, bo te testy maja docelowo mieć zawsze pozytywny wynik, tak?
    def test_date_of_death_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEquals(field_label, 'Data śmierci')

    # TODO 2. Napisz test sprawdzający czy wartość parametru max_length dla pola surname jest równa 100.
    def test_surname_max_length_(self):
        author = Author.objects.get(id=1)
        field_max_length = author._meta.get_field('surname').max_length
        self.assertEquals(field_max_length, 100)
