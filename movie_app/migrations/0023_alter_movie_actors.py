# Generated by Django 5.0 on 2023-12-22 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_app', '0022_alter_movie_director'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='actors',
            field=models.ManyToManyField(related_name='movies', to='movie_app.actor'),
        ),
    ]
