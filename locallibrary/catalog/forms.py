from datetime import date, timedelta
from django import forms
from django.contrib.auth.models import User
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

        # if the form submitted and the model instance exists,
        # clean the book instance borrower in the database
        if self.is_bound and self.instance.pk:
            self.instance.borrower = None
            self.instance.save()


class BookInstanceChangeStatusForm(forms.ModelForm):
    class Meta:
        model = BookInstance
        fields = ['status', 'borrower', 'due_back']
        # TODO co robia te podkreślniki tutaj?
        labels = {'borrower': _('Użytkownik'), 'due_back': _('Maksymalna data zwrotu')}
        help_texts = {'due_back': _('Wprowadz date w zakresie od dzis do 31 dni dni (domyslnie 30 dni od dzis.')}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['borrower'].empty_label = None

        if self.is_bound and self.fields['status']==(('a', 'Dostępna') or ('m', 'W trakcie renowacji')):
            self.instance.borrower = None
            self.instance.save()

    def get_initial(self):
        initial = super().get_initial()
        initial['due_back'] = date.today() + timedelta(days=30)
        return initial

    def clean_due_back(self):
        data = self.cleaned_data['due_back']

        if data < date.today():
            raise ValidationError(_('Niepoprawna data - data z przeszłości'))

        if data > date.today() + timedelta(days=31):
            raise ValidationError(_('Książke można wypozyczyc na nie więcej niż 31 dni'))
        return data


class BookInstanceBorrowForm(BookInstanceChangeStatusForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user=user
        status_choices = [('r', 'Zarezerwuj'), ('o', 'Wypożycz')]
        self.fields['status'].choices = status_choices
        self.fields['borrower'].queryset = User.objects.filter(username=user)

    def get_initial(self):
        initial = super().get_initial()
        initial['status'] = 'o'
        return initial


class BookInstanceReserveForm(BookInstanceChangeStatusForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        status_choices = [('r', 'Zarezerwuj'), ('o', 'Wypożycz')]
        self.fields['status'].choices = status_choices
        self.fields['borrower'].queryset = User.objects.filter(username=user)

    def get_initial(self):
        initial = super().get_initial()
        initial['status'] = 'r'
        return initial

