# Generated by Django 3.1.7 on 2021-03-26 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0009_auto_20210324_0151'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookinstance',
            name='fake',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Fake'),
        ),
    ]
