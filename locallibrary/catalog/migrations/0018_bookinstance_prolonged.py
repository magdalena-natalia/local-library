# Generated by Django 3.1.7 on 2021-04-29 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0017_bookinstance_borrower'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookinstance',
            name='prolonged',
            field=models.BooleanField(default=False),
        ),
    ]