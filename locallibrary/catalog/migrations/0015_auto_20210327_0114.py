# Generated by Django 3.1.7 on 2021-03-27 01:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0014_auto_20210327_0112'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back'], 'permissions': (('can_mark_returned', 'Can set book as returned'),)},
        ),
    ]
