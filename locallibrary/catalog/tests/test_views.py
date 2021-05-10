from django.test import TestCase
from django.urls import reverse
from catalog.models import Author


class AuthorListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Tworzenie 13 autorów na potrzeby testowania paginacji
        number_of_authors = 13

        for author_id in range(number_of_authors):
            Author.objects.create(
                names=f'Joe{author_id}',
                surname=f'Doe {author_id}',
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/catalog/authors/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)

    def test_lists_all_authors(self):
        # Pobranie drugiej strony dla potwierdzenia ze ma dokladnie 3 autorow
        response = self.client.get(reverse('authors') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertTrue(len(response.context['author_list']) == 3)

    # TODO 1. Napisz test sprawdzający czy wartość paginacji wynosi 10.
    def test_paginated_by_ten(self):
        response = self.client.get(reverse('authors'))
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(len(response.context['author_list']) == 10)

    # # TODO 2. Napisz test sprawdzający czy widok używa poprawnego wzorca html np. author_list.html.
    def test_html(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.template_name, ['author_list.html', 'catalog/author_list.html'])


    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'author_list.html')
