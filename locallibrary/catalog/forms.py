from datetime import date, timedelta
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from catalog.models import BookInstance


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text='Wprowadz datę w zakresie od dzis do 31 dni (domyslnie 30 dni).')

    def clean_renewal_date(self):
        # TODO czy renew_date - opisowa nazwa zmiennej - może byc czy raczej data jest tu zwyczajowe?
        renew_date = self.cleaned_data['renewal_date']
        if renew_date < date.today():
            raise ValidationError(_('Niepoprawna data - data sprzed dnia dzisiejszego.'))
        if renew_date > date.today() + timedelta(days=31):
            raise ValidationError(_("Niepoprawna data. Dozwolone do 31 dni liczonych od dziś."))
        return renew_date


class BookInstanceReturnForm(forms.ModelForm):
    class Meta:
        model = BookInstance
        fields = ['status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        userless_choices = [('a', 'Dostępna'), ('m', 'W trakcie renowacji')]
        self.fields['status'].choices = userless_choices
        # self.fields['status'].default = 'a'

        # if the form submitted and the model instance exists,
        # clean the book instance borrower in the database
        if self.is_bound and self.instance.pk:
            self.instance.borrower = None
            self.instance.save()
