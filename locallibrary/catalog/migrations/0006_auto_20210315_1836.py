# Generated by Django 3.1.7 on 2021-03-15 17:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_auto_20210315_1820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='first_published',
            field=models.IntegerField(help_text='Wprowadz rok pierwszego oryginalnego wydania, z "-", jeśli p.n.e.', validators=[django.core.validators.MaxValueValidator(limit_value=2021, message='Rok nie moze byc pozniejszy od biezacego.')], verbose_name='Data pierwszego wydania'),
        ),
        migrations.AlterField(
            model_name='book',
            name='isbn',
            field=models.IntegerField(help_text='13-cyfrowy <a href="https://www.isbn-international.org/content/what-isbn">numer ISBN</a>', validators=[django.core.validators.MinValueValidator(limit_value=1000000000000, message='Wpisz same cyfry z numeru ISBN, powinno ich byc dokladnie 13.'), django.core.validators.MaxValueValidator(9999999999999, message='Wpisz same cyfry z numeru ISBN, powinno ich byc dokladnie 13.')], verbose_name='ISBN'),
        ),
    ]
