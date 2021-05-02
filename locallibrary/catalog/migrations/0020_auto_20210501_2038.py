# Generated by Django 3.1.7 on 2021-05-01 20:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0019_auto_20210501_2034'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ['surname']},
        ),
        migrations.AlterModelOptions(
            name='book',
            options={},
        ),
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back'], 'permissions': (('can_mark_returned', 'Can set book as returned'),)},
        ),
    ]
