import datetime
from django.test import TestCase
from catalog.forms import RenewBookForm
from django.utils import timezone


class RenewBookFormTest(TestCase):
    def test_renew_form_date_field_label(self):
        form = RenewBookForm()
        self.assertTrue(form.fields['renewal_date'].label is None or form.fields['renewal_date'].label == 'Przedłuż do')

    def test_renew_form_date_in_past(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertFalse(form.is_valid())

    def test_renew_form_date_max(self):
        date = timezone.localtime() + datetime.timedelta(weeks=4)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertTrue(form.is_valid())

    # TODO 1. Napisz test, który przy użyciu modelu datetime sprawdzi czy formularz zwrócił wartość False dla terminu wypożyczenia dłuższego niż 4 tygodnie.
    def test_renew_form_date_5_weeks(self):
        date = datetime.date.today() + datetime.timedelta(weeks=5)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertFalse(form.is_valid())

    def test_renew_form_date_32_days(self):
        date = datetime.date.today() + datetime.timedelta(days=32)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertFalse(form.is_valid())

    # TODO 2. Napisz test, który sprawdzi czy podana dzisiejsza data jako wartość renewal_date jest poprawna i formularz zwróci True.
    def test_renew_form_date_today(self):
        date = datetime.date.today()
        form = RenewBookForm(data={'renewal_date': date})
        self.assertTrue(form.is_valid())
