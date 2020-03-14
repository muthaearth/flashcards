# Generated by Django 3.0.4 on 2020-03-14 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flashcards', '0002_auto_20200314_1705'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flashcard',
            name='deck',
        ),
        migrations.AddField(
            model_name='deck',
            name='flashcards',
            field=models.ManyToManyField(to='flashcards.FlashCard'),
        ),
    ]
