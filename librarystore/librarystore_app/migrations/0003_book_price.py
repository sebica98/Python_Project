# Generated by Django 4.0.2 on 2022-04-11 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('librarystore_app', '0002_navbar'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='price',
            field=models.FloatField(default=4.99),
        ),
    ]
