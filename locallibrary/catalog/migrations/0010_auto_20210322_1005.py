# Generated by Django 3.1.7 on 2021-03-22 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0009_auto_20210321_2136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='bio',
            field=models.TextField(blank=True, help_text='Wprowadz krotki zyciorys i charakterystyke autora', null=True, verbose_name='Notka biograficzna'),
        ),
    ]
