# Generated by Django 3.1.7 on 2021-03-26 19:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0010_bookinstance_fake'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookinstance',
            name='fake',
        ),
    ]
