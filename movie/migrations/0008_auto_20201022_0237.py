# Generated by Django 3.1.2 on 2020-10-22 02:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0007_auto_20201022_0210'),
    ]

    operations = [
        migrations.RenameField(
            model_name='genres',
            old_name='genre',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='moviegenres',
            old_name='title',
            new_name='movie',
        ),
        migrations.RenameField(
            model_name='services',
            old_name='service',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='tags',
            old_name='tag',
            new_name='name',
        ),
    ]
