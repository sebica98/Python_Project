# Generated by Django 4.0.2 on 2022-06-02 09:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('librarystore_app', '0010_book_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='navbar',
            options={'ordering': ['id']},
        ),
    ]