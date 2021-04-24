from datetime import date, timedelta
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text='Wprowadz datę w zakresie od dzis do 31 dni (domyslnie 30 dni).')

    def clean_renewal_date(self):
        renew_date = self.cleaned_data['renewal_date']
        if renew_date < date.today():
            raise ValidationError(_('Niepoprawna data - data sprzed dnia dzisiejszego.'))
        if renew_date > date.today() + timedelta(days=31):
            raise ValidationError(_("Niepoprawna data. Dozwolone do 31 dni liczonych od dziś."))
        return renew_date


