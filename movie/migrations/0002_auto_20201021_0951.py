# Generated by Django 3.1.2 on 2020-10-21 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movies',
            name='casting',
            field=models.ManyToManyField(null=True, related_name='people', through='movie.Cast', to='movie.People'),
        ),
    ]